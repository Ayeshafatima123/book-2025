"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateSpecificToken = void 0;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
// Function to validate the specific JWT token you provided
const validateSpecificToken = (token) => {
    const expectedToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.buTF0xgOeAnfMRkQh8PcVb6xC4IoYF-Bp0P4sqhn7mA';
    if (token !== expectedToken) {
        return false;
    }
    // Use the same secret that was used to generate the token
    // The token 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.buTF0xgOeAnfMRkQh8PcVb6xC4IoYF-Bp0P4sqhn7mA'
    // was created with the secret 'your-jwt-secret-here' based on the .env file
    try {
        const decoded = jsonwebtoken_1.default.verify(token, process.env.JWT_SECRET || 'your-jwt-secret-here');
        return decoded.access === 'm';
    }
    catch (error) {
        console.error('Token validation error:', error);
        return false;
    }
};
exports.validateSpecificToken = validateSpecificToken;
