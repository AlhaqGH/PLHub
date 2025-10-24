"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PohLangDiagnostics = void 0;
const vscode = __importStar(require("vscode"));
const processUtils_1 = require("../utils/processUtils");
class PohLangDiagnostics {
    constructor(context) {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('pohlang');
        context.subscriptions.push(this.diagnosticCollection);
        // Register event listeners
        vscode.workspace.onDidChangeTextDocument(this.onDocumentChange, this, context.subscriptions);
        vscode.workspace.onDidOpenTextDocument(this.onDocumentOpen, this, context.subscriptions);
    }
    onDocumentChange(event) {
        if (event.document.languageId === 'pohlang') {
            this.updateDiagnostics(event.document.uri);
        }
    }
    onDocumentOpen(document) {
        if (document.languageId === 'pohlang') {
            this.updateDiagnostics(document.uri);
        }
    }
    async updateDiagnostics(uri) {
        const document = await vscode.workspace.openTextDocument(uri);
        if (document.languageId !== 'pohlang') {
            return;
        }
        const diagnostics = [];
        try {
            // Basic syntax validation
            const syntaxErrors = this.validateSyntax(document);
            diagnostics.push(...syntaxErrors);
            // Try to run syntax check with interpreter (if available)
            const interpreterErrors = await this.validateWithInterpreter(uri.fsPath);
            diagnostics.push(...interpreterErrors);
        }
        catch (error) {
            // If interpreter validation fails, that's okay - we'll just use basic validation
        }
        this.diagnosticCollection.set(uri, diagnostics);
    }
    validateSyntax(document) {
        const diagnostics = [];
        const text = document.getText();
        const lines = text.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            const lineNumber = i;
            // Skip empty lines and comments
            if (!line || line.startsWith('#')) {
                continue;
            }
            // Check for common syntax issues
            this.checkFunctionDefinition(line, lineNumber, diagnostics);
            this.checkVariableAssignment(line, lineNumber, diagnostics);
            this.checkControlStructures(line, lineNumber, diagnostics);
            this.checkStringQuotes(line, lineNumber, diagnostics);
        }
        return diagnostics;
    }
    checkFunctionDefinition(line, lineNumber, diagnostics) {
        const functionRegex = /^(make\s+function\s+\w+:|function\s+\w+:)/;
        if (line.includes('function') && !functionRegex.test(line)) {
            const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, line.length), 'Invalid function definition. Use "make function name:" or "function name:"', vscode.DiagnosticSeverity.Error);
            diagnostics.push(diagnostic);
        }
    }
    checkVariableAssignment(line, lineNumber, diagnostics) {
        if (line.includes('set') && !line.includes('to')) {
            const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, line.length), 'Variable assignment should use "set variable to value" syntax', vscode.DiagnosticSeverity.Warning);
            diagnostics.push(diagnostic);
        }
    }
    checkControlStructures(line, lineNumber, diagnostics) {
        const controlKeywords = ['if', 'while', 'for'];
        for (const keyword of controlKeywords) {
            if (line.startsWith(keyword) && !line.endsWith(':')) {
                const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, line.length), `${keyword} statement should end with a colon (:)`, vscode.DiagnosticSeverity.Error);
                diagnostics.push(diagnostic);
            }
        }
    }
    checkStringQuotes(line, lineNumber, diagnostics) {
        // Check for unmatched quotes
        const singleQuotes = (line.match(/'/g) || []).length;
        const doubleQuotes = (line.match(/"/g) || []).length;
        if (singleQuotes % 2 !== 0) {
            const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, line.length), 'Unmatched single quote', vscode.DiagnosticSeverity.Error);
            diagnostics.push(diagnostic);
        }
        if (doubleQuotes % 2 !== 0) {
            const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, line.length), 'Unmatched double quote', vscode.DiagnosticSeverity.Error);
            diagnostics.push(diagnostic);
        }
    }
    async validateWithInterpreter(filePath) {
        const diagnostics = [];
        try {
            // Try to run syntax check with the interpreter
            const result = await (0, processUtils_1.spawnPohLangProcess)(filePath, ['--syntax-check']);
            if (!result.success && result.stderr) {
                // Parse interpreter error messages
                const errorMessages = this.parseInterpreterErrors(result.stderr);
                diagnostics.push(...errorMessages);
            }
        }
        catch (error) {
            // Interpreter not available or failed - ignore
        }
        return diagnostics;
    }
    parseInterpreterErrors(errorOutput) {
        const diagnostics = [];
        const lines = errorOutput.split('\n');
        for (const line of lines) {
            // Parse error format: "Line X: Error message"
            const match = line.match(/Line (\d+):\s*(.+)/);
            if (match) {
                const lineNumber = parseInt(match[1]) - 1; // Convert to 0-based
                const message = match[2];
                const diagnostic = new vscode.Diagnostic(new vscode.Range(lineNumber, 0, lineNumber, Number.MAX_SAFE_INTEGER), message, vscode.DiagnosticSeverity.Error);
                diagnostics.push(diagnostic);
            }
        }
        return diagnostics;
    }
    dispose() {
        this.diagnosticCollection.dispose();
    }
}
exports.PohLangDiagnostics = PohLangDiagnostics;
//# sourceMappingURL=diagnostics.js.map