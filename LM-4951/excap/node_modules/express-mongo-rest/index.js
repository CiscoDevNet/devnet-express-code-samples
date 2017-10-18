var express = require('express')
var mongoskin = require('mongoskin')
var ObjectID = require('mongodb').ObjectID
var patch2m = require('jsonpatch-to-mongodb')
var query2m = require('query-to-mongo')
var bodyParser = require('body-parser')
var inflector = require('inflection')

module.exports = function expressMongodbRest(db, options) {
    var router

    if (!db) throw new TypeError('db required')
    if (typeof db === 'string') db = mongoskin.db(db, {safe: true})
    options = options || {}

    router = express.Router()
    router.db = db

    router.use(bodyParser.json())
    router.use(function (req, res, next) {
        req.db = router.db
        res.envelope = options.envelope
        next()
    })

    if (options.validator) router.use(options.validator)

    addRestMethods(router, options.singularize || inflector.singularize)
    router.use('/:collection', convertId)
    router.use('/:collection', envelope)
    router.use('/:collection', sendJson)
    return router
}

function isEmpty(obj) {
    if (obj == null || obj.length === 0) return true
    if (obj.length > 0) return false
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) return false
    }
    return true
}

function fullUrl(req) {
    return req.protocol + '://' + req.get('host') + req.originalUrl
}

function normalizeId(id) {
    if (ObjectID.isValid(id)) return new ObjectID(id)
    return id;
}

function addRestMethods(router, singularize) {
    router.param('collection', function collectionParam(req, res, next, collection) {
        res.locals.plural = collection
        res.locals.singular = singularize(collection)
        req.collection = req.db.collection(res.locals.plural)
        next()
    })

    router.param('id', function (req, res, next, id) {
        req.idMatch = { _id: normalizeId(id) }
        next()
    })

    router.get('/:collection', function (req, res, next) {
        var query = query2m(req.query, { ignore: 'envelope' })

        req.collection.count(query.criteria, function (e, count) {
            var links
            if (e) return next(e)
            res.append('X-Total-Count', count)
            links = query.links(fullUrl(req), count)
            if (links) res.links(links)
            req.collection.find(query.criteria, query.options).toArray(function (e, results) {
                if (e) return next(e)
                res.locals.json = results
                next()
            })
        })
    })

    router.post('/:collection', function (req, res, next) {
        if (!req.body || isEmpty(req.body)) throw { status: 400, message: 'No Request Body' } // Bad Request
        req.collection.insert(req.body, function (e, result) {
            if (e) return next(e)
            res.append('Location', fullUrl(req) + '/' + result.ops[0]._id)
            res.status(201) // Created
            res.locals.json = result.ops[0]
            next()
        })
    })

    router.put('/:collection', function (req, res, next) {
        // TODO: bulk update?
        res.status(405).send() // Method Not Allowed
    })

    router.patch('/:collection', function (req, res, next) {
        res.status(405).send() // Method Not Allowed
    })

    router.delete('/:collection', function (req, res, next) {
        req.collection.remove({}, null, function (e, result) {
            if (e) return next(e)
            res.status(204).send() // No Content
        })
    })

    router.get('/:collection/:id', function (req, res, next) {
        req.collection.findOne(req.idMatch, function (e, result) {
            if (e) return next(e)
            if (!result) res.status(404) // Not Found
            res.locals.json = result
            next()
        })
    })

    router.post('/:collection/:id', function (req, res, next) {
        res.status(405).send() // Method Not Allowed
    })

    router.put('/:collection/:id', function (req, res, next) {
        if (!req.body || isEmpty(req.body)) throw { status: 400, message: 'No Request Body' } // Bad Request
        req.body._id = normalizeId(req.params.id)
        req.collection.update(req.idMatch, req.body, { upsert: true }, function (e, result) {
            if (e) return next(e)
            // mongodb's update with $set/$unset doesn't error if there's no match
            // and doesn't return a result upon success; but a findOne after will
            req.collection.findOne(req.idMatch, function (e, result) {
                if (e) return next(e)
                res.locals.json = result
                next()
            })
        })
    })

    router.patch('/:collection/:id', function (req, res, next) {
        if (!req.body || isEmpty(req.body)) throw { status: 400, message: 'No Request Body' } // Bad Request
        req.collection.update(req.idMatch, patch2m(req.body), function (e, result) {
            if (e) return next(e)
            // mongodb's update with $set/$unset doesn't error if there's no match
            // and doesn't return a result upon success; but a findOne after will
            req.collection.findOne(req.idMatch, function (e, result) {
                if (e) return next(e)
                res.locals.json = result
                next()
            })
        })
    })

    router.delete('/:collection/:id', function (req, res, next) {
        req.collection.remove(req.idMatch, { single: true }, function (e, result) {
            if (e) return next(e)
            res.status(204).send(); // No Content
        })
    })

    // TODO: sub-resources (ie., get/post on /:collection/:id/resource)

    return router
}

function convertId(req, res, next) {
    if (res.locals.json instanceof Array) {
        res.locals.json.forEach(renameIdKey)
    } else if (res.locals.json) {
        renameIdKey(res.locals.json)
    }
    next()
}

function renameIdKey(obj) {
    if (obj) {
        obj.id = obj._id
        delete obj._id
    }
    return obj
}

function isToggled(value, override) {
    return (override && override === String(!value))
}

function envelope(req, res, next) {
    var useEnvelope = res.envelope
    if (isToggled(useEnvelope, req.query['envelope'])) useEnvelope = !useEnvelope

    if (useEnvelope && res.locals.json) {
        var envelope = {}
        var type = res.locals.singular
        if (res.locals.json instanceof Array) type = res.locals.plural
        envelope[type] = res.locals.json
        res.locals.json = envelope
    }
    next()
}

function sendJson(req, res, next) {
    if (res.locals.json) res.send(res.locals.json)
    else next()
}
