#!/usr/bin/env node

var express = require('express')
var compress = require('compression')
var methodOverride = require('method-override')
var expressMongodbRest = require('./index')
var https = require('https')
var pem = require('pem')
var fs = require('fs')
var dotenv = require('dotenv')

dotenv.load()

var port = normalizePort(process.env.PORT || '3000')
var db = process.env.DB || 'mongodb://localhost:27017/express-mongo-rest'

// recommended to mitigate against BEAST attack (see https://community.qualys.com/blogs/securitylabs/2011/10/17/mitigating-the-beast-attack-on-tls)
var ciphers = 'ECDHE-RSA-AES128-SHA256:AES128-GCM-SHA256:RC4:HIGH:!MD5:!aNULL:!EDH'

try {
    if (process.env.PFX) {
        var options = {
            pfx: fs.readFileSync(process.env.PFX),
            passphrase: process.env.PASSPHRASE,
            ciphers: ciphers,
            honorCipherOrder: true
        }
        createServer(options, port, db)
    } else if (process.env.KEY || process.env.CERT) {
        if (!process.env.KEY) throw 'CERT defined, but KEY is not'
        if (!process.env.CERT) throw 'KEY defined, but CERT is not'
        var options = {
            key: fs.readFileSync(process.env.KEY),
            cert: fs.readFileSync(process.env.CERT),
            passphrase: process.env.PASSPHRASE,
            ciphers: ciphers,
            honorCipherOrder: true
        }
        createServer(options, port, db)
    } else {
        pem.createCertificate({days: 9999, selfSigned: true}, function (err, keys) {
            var options = {
                key: keys.serviceKey,
                cert: keys.certificate,
                ciphers: ciphers,
                honorCipherOrder: true
            }
            if (err) throw (err)
            createServer(options, port, db)
        })
    }
} catch (err) {
    console.error(err.message || err)
}

function createServer(options, port, db) {
    var app, server

    app = express()
    app.use(compress())
    app.use(methodOverride())
    app.use('/api/v1', expressMongodbRest(db))
    app.set('port', port)
    app.set('json spaces', 2)
    app.set('query parser', 'simple')

    server = https.createServer(options, app)
    server.listen(port, function() {
        var addr = server.address()
        var bind = (typeof addr === 'string') ? 'pipe ' + addr : 'port ' + addr.port
        console.info('Listening on ' + bind)
    })

    server.on('error', onError)
}

function normalizePort(val) {
    var port = parseInt(val, 10);
    if (isNaN(port)) return val
    return (port >= 0) ? port : false
}

function onError(err) {
    if (err.syscall !== 'listen') throw err

    var bind = (typeof port === 'string') ? 'pipe ' + port : 'port ' + port

    switch (err.code) {
        case 'EACCES':
            console.error('EACCESS, ' + bind + ' requires elevated privileges')
            break;
        case 'EADDRINUSE':
            console.error('EADDRINUSE, ' + bind + ' is already in use')
            break;
        default:
            throw err
    }
}
