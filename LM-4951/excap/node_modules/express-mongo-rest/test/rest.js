var assert = require('chai').assert
var expressMongoRest = require('../index')
var express = require('express')
var mongoskin = require('mongoskin')
var ObjectID = require('mongodb').ObjectID
var http = require('http')
var request = require('supertest')

function createApp(db) {
    var app = express()
    var router = expressMongoRest(db)
    app.use('/api/v1', router)
    app.db = router.db

    app.use(function(err, req, res, next) {
        if (!err.status) console.error(err)
        res.status(err.status || 500)
        res.setHeader('Content-Type', 'application/json')
        res.send(err)
    })
    return app
}

describe('express-rest-mongo', function () {
    var app, db

    app = createApp('mongodb://localhost:27017/express-rest-mongo-test')
    db = app.db
    db.bind('users')

    after(function (done) {
        db.dropDatabase(function (err) { db.close(done) })
    })

    describe('/:collection', function () {
        beforeEach(function (done) {
            db.users.remove({}, null, function (err) {
                if (err) throw done(err)
                var list = [{_id:'0001', name:'Bob', email:'bob@example.com'}, {name:'Judy', email:'judy@example.com'}]
                db.users.insert(list, null, done)
            })
        })

        describe('GET', function () {
            it('should find all', function (done) {
                request(app).get('/api/v1/users')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.equal(result.length, 2)
                        assert.equal(res.headers['x-total-count'], 2)
                        assert.notOk(result[0]._id, 'do not expect _id')
                        assert.notOk(result[1]._id, 'do not expect _id')
                        assert.ok(result[0].id, 'expect id')
                        assert.ok(result[1].id, 'expect id')
                        done()
                    })
            })
            it('should find by query', function (done) {
                request(app).get('/api/v1/users?name=Bob')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.equal(result.length, 1)
                        assert.equal(res.headers['x-total-count'], 1)
                        assert.equal(result[0].name, 'Bob')
                        assert.notOk(result[0]._id, 'do not expect _id')
                        assert.ok(result[0].id, 'expect id')
                        done()
                    })
            })
            it('should find none by query', function (done) {
                request(app).get('/api/v1/users?name=None')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.equal(result.length, 0)
                        assert.equal(res.headers['x-total-count'], 0)
                        done()
                    })
            })
            it('can return an envelope', function (done) {
                request(app).get('/api/v1/users?name=Bob&envelope=true')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.equal(res.headers['x-total-count'], 1)
                        assert.ok(result.users, 'expect envelope')
                        assert.equal(result.users.length, 1)
                        assert.equal(result.users[0].name, 'Bob')
                        assert.notOk(result.users[0]._id, 'do not expect _id')
                        assert.ok(result.users[0].id, 'expect id')
                        done()
                    })
            })
        })

        describe('POST', function () {
            it('should create document', function (done) {
                request(app).post('/api/v1/users')
                    .set('Content-Type', 'application/json')
                    .send({name:'Carl', email:'carl@example.com'})
                    .expect(201)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.notOk(result._id, 'do not expect _id')
                        assert.ok(result.id, 'expect id')
                        done()
                    })
            })
            it('should fail w/o body', function (done) {
                request(app).post('/api/v1/users')
                    .set('Content-Type', 'application/json')
                    .expect(400)
                    .send()
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
            it('can return an envelope', function (done) {
                request(app).post('/api/v1/users?envelope=true')
                    .set('Content-Type', 'application/json')
                    .send({name:'Carl', email:'carl@example.com'})
                    .expect(201)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.ok(result.user, 'expect envelope')
                        assert.notOk(result.user._id, 'do not expect _id')
                        assert.ok(result.user.id, 'expect id')
                        done()
                    })
            })
        })

        describe('PUT', function () {
            it('should fail w/o full path', function (done) {
                request(app).put('/api/v1/users')
                    .set('Content-Type', 'application/json')
                    .send({name:'Carl', email:'carl@example.com'})
                    .expect(405)
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
        })

        describe('PATCH', function () {
            it('should fail w/o full path', function (done) {
                request(app).patch('/api/v1/users')
                    .set('Content-Type', 'application/json')
                    .send([
                        { op: "replace", path:'/name', value:'Bobby' },
                        { op: "replace", path:'/email', value:'bobby@example.com' }
                    ])
                    .expect(405)
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
        })

        describe('DELETE', function () {
            it('should remove all', function (done) {
                db.users.count({}, function (e, result) {
                    assert.notEqual(result, 0, 'expect some to exist');
                    request(app).delete('/api/v1/users')
                        .set('Content-Type', 'application/json')
                        .expect(204)
                        .end(function(err, res) {
                            if (err) return done(err)
                            db.users.count({}, function (e, result) {
                                assert.equal(result, 0);
                                done()
                            })
                        })
                })
            })
        })
    })

    describe('/:collection/:id', function () {
        beforeEach(function (done) {
            db.users.remove({}, null, function () {
                var list = [{_id:'0001', name:'Bob', email:'bob@example.com'}, {name:'Judy', email:'judy@example.com'}]
                db.users.insert(list, null, done)
            })
        })

        describe('GET', function () {
            it('should find one', function (done) {
                request(app).get('/api/v1/users/0001')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.notOk(result._id, 'do not expect _id')
                        assert.equal(result.id, '0001')
                        assert.equal(result.name, 'Bob')
                        done()
                    })
            })
            it('should find one by generated id', function (done) {
                db.users.findOne({name:'Judy'}, function (e, result) {
                    var id = result._id
                    request(app).get('/api/v1/users/' + id)
                        .expect(200)
                        .end(function(err, res) {
                            if (err) return done(err)
                            var result = JSON.parse(res.text)
                            assert.notOk(result._id, 'do not expect _id')
                            assert.equal(result.id, id)
                            assert.equal(result.name, 'Judy')
                            done()
                        })
                })
            })
            it('should find none by id', function (done) {
                request(app).get('/api/v1/users/none')
                    .expect(404)
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
            it('can return an envelope', function (done) {
                request(app).get('/api/v1/users/0001?envelope=true')
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.ok(result.user, 'expect envelope')
                        assert.notOk(result.user._id, 'do not expect _id')
                        assert.equal(result.user.id, '0001')
                        assert.equal(result.user.name, 'Bob')
                        done()
                    })
            })
        })

        describe('POST', function () {
            it('should fail w/ full path', function (done) {
                request(app).post('/api/v1/users/0001')
                    .set('Content-Type', 'application/json')
                    .expect(405)
                    .send()
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
        })

        describe('PUT', function () {
            it('should update document', function (done) {
                request(app).put('/api/v1/users/0001')
                    .set('Content-Type', 'application/json')
                    .send({name:'Bobby', email:'bobby@example.com'})
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.equal(result.id, '0001')
                        assert.notOk(result._id);
                        db.users.findOne({_id: '0001'}, function (e, result) {
                            assert.equal(result.name, 'Bobby');
                            done()
                        })
                    })
            })
            it('should update document by generated id', function (done) {
                db.users.findOne({name:'Judy'}, function (e, result) {
                    var id = result._id
                    request(app).put('/api/v1/users/' + id)
                        .set('Content-Type', 'application/json')
                        .send({name:'Judith', email:'judith@example.com'})
                        .expect(200)
                        .end(function(err, res) {
                            if (err) return done(err)
                            var result = JSON.parse(res.text)
                            assert.notOk(result._id, 'do not expect _id')
                            assert.equal(result.id, id)
                            db.users.findOne({_id: id}, function (e, result) {
                                assert.equal(result.name, 'Judith');
                                done()
                            })
                        })
                })
            })
            it('should create document', function (done) {
                request(app).put('/api/v1/users/0002')
                    .set('Content-Type', 'application/json')
                    .send({name:'Carl', email:'carl@example.com'})
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.notOk(result._id, 'do not expect _id')
                        assert.equal(result.id, '0002')
                        db.users.findOne({_id: '0002'}, function (e, result) {
                            assert.equal(result.name, 'Carl');
                            done()
                        })
                    })
            })
            it('should fail w/o body', function (done) {
                request(app).put('/api/v1/users/0')
                    .set('Content-Type', 'application/json')
                    .expect(400)
                    .send()
                    .end(function(err, res) {
                        if (err) return done(err)
                        done()
                    })
            })
            it('can return an envelope', function (done) {
                request(app).put('/api/v1/users/0001?envelope=true')
                    .set('Content-Type', 'application/json')
                    .send({name:'Bobby', email:'bobby@example.com'})
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.ok(result.user, 'expect envelope')
                        assert.equal(result.user.id, '0001')
                        assert.notOk(result.user._id);
                        db.users.findOne({_id: '0001'}, function (e, result) {
                            assert.equal(result.name, 'Bobby');
                            done()
                        })
                    })
            })
        })

        describe('PATCH', function () {
            it('should update document', function (done) {
                request(app).patch('/api/v1/users/0001')
                    .set('Content-Type', 'application/json')
                    .send([
                        { op: "replace", path:'/name', value:'Bobby' },
                        { op: "replace", path:'/email', value:'bobby@example.com' }
                    ])
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.notOk(result._id, 'do not expect _id')
                        assert.equal(result.id, '0001')
                        db.users.findOne({_id: '0001'}, function (e, result) {
                            assert.equal(result.name, 'Bobby');
                            done()
                        })
                    })
            })
            it('can return an envelope', function (done) {
                request(app).patch('/api/v1/users/0001?envelope=true')
                    .set('Content-Type', 'application/json')
                    .send([
                        { op: "replace", path:'/name', value:'Bobby' },
                        { op: "replace", path:'/email', value:'bobby@example.com' }
                    ])
                    .expect(200)
                    .end(function(err, res) {
                        if (err) return done(err)
                        var result = JSON.parse(res.text)
                        assert.ok(result.user, 'expect envelope')
                        assert.notOk(result.user._id, 'do not expect _id')
                        assert.equal(result.user.id, '0001')
                        db.users.findOne({_id: '0001'}, function (e, result) {
                            assert.equal(result.name, 'Bobby');
                            done()
                        })
                    })
            })
        })

        describe('DELETE', function () {
            it('should remove document', function (done) {
                db.users.count({name: 'Bob'}, function (e, result) {
                    assert.equal(result, 1, 'expect match to exist');

                    request(app).delete('/api/v1/users/0001')
                        .set('Content-Type', 'application/json')
                        .expect(204)
                        .end(function(err, res) {
                            if (err) return done(err)
                            db.users.count({name: 'Bob'}, function (e, result) {
                                assert.equal(result, 0);
                                done()
                            })
                        })
                })
            })

            it('should remove document by generated id', function (done) {
                db.users.findOne({name:'Judy'}, function (e, result) {
                    var id = result._id
                    assert.ok(id, 'expect match to exist');
                    request(app).delete('/api/v1/users/' + id)
                        .expect(204)
                        .end(function(err, res) {
                            if (err) return done(err)
                            db.users.count({name: 'Judy'}, function (e, result) {
                                assert.equal(result, 0);
                                done()
                            })
                        })
                })
            })
        })
    })
})
