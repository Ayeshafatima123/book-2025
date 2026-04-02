"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateJWT = void 0;
const jwt_validator_1 = require("./jwt-validator");
// JWT authentication middleware
const authenticateJWT = (req, res, next) => {
    // Allow health checks without authentication
    if (req.path === '/health' && req.method === 'GET') {
        return next();
    }
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
    if (!token) {
        return res.status(401).json({
            error: 'Access token required'
        });
    }
    // Validate the specific token provided by the user
    if (!(0, jwt_validator_1.validateSpecificToken)(token)) {
        return res.status(403).json({
            error: 'Invalid or unauthorized token'
        });
    }
    // Token is valid, continue with request
    next();
};
exports.authenticateJWT = authenticateJWT;
