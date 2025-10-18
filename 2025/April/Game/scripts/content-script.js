// Check if link is like: https://norstatsurveys.com/wix/3/p940507710843.aspx

// Custom Bytecode DOM Interpreter by Claude

class BytecodeInterpreter {
    constructor() {
        // Bytecode operation types
        this.OP_CODES = {
            SET_VALUE: 'SET_VALUE',
            DISPATCH_EVENT: 'DISPATCH_EVENT',
            SET_ATTRIBUTE: 'SET_ATTRIBUTE',
            CLICK_ELEMENT: 'CLICK_ELEMENT'
        };
    }

    /**
     * Find element using a flexible selector
     * @param {string} selector - CSS selector or ID
     * @returns {Element|null} Found element or null
     */
    findElement(selector) {
        if (selector.startsWith('##')) {
            selector = selector.substring(2);
            return document.getElementById(selector);
        }

        if (selector.startsWith('#') && !selector.includes(' ')) {
            return document.getElementById(selector.substring(1));
        }

        return document.querySelector(selector);
    }

    /**
     * Execute a single bytecode instruction
     * @param {string} instruction - Bytecode instruction
     */
    executeInstruction(instruction) {
        // Split instruction into parts
        const parts = instruction.split(/\s+(?=(?:[^"]*"[^"]*")*[^"]*$)/);
        const opCode = parts[0];
        
        // Remove quotes from selector and value
        const selector = parts[1].replace(/^"|"$/g, '');
        const value = parts[2] ? parts[2].replace(/^"|"$/g, '') : null;

        switch (opCode) {
            case this.OP_CODES.SET_VALUE:
                this.setValue(selector, value);
                break;
            case this.OP_CODES.DISPATCH_EVENT:
                this.dispatchEvent(selector, value);
                break;
            case this.OP_CODES.SET_ATTRIBUTE:
                // Assuming third param is attribute name, fourth is value
                const attrName = value;
                const attrValue = parts[3] ? parts[3].replace(/^"|"$/g, '') : null;
                this.setAttribute(selector, attrName, attrValue);
                break;
            case this.OP_CODES.CLICK_ELEMENT:
                this.clickElement(selector);
                break;
            default:
                console.error('Unknown operation code:', opCode);
        }
    }

    /**
     * Set value of an input element
     * @param {string} selector - Selector for the element
     * @param {string} value - Value to set
     */
    setValue(selector, value) {
        const element = this.findElement(selector);
        if (element && 'value' in element) {
            element.value = value;
        } else {
            console.error(`Cannot set value for element: ${selector}`);
        }
    }

    /**
     * Dispatch an event on an element
     * @param {string} selector - Selector for the element
     * @param {string} eventType - Type of event to dispatch
     */
    dispatchEvent(selector, eventType) {
        const element = this.findElement(selector);
        if (element) {
            const event = new Event(eventType, { bubbles: true });
            element.dispatchEvent(event);
        } else {
            console.error(`Cannot dispatch event for element: ${selector}`);
        }
    }

    /**
     * Set an attribute on an element
     * @param {string} selector - Selector for the element
     * @param {string} attributeName - Name of the attribute
     * @param {string} attributeValue - Value of the attribute
     */
    setAttribute(selector, attributeName, attributeValue) {
        const element = this.findElement(selector);
        if (element) {
            element.setAttribute(attributeName, attributeValue);
        } else {
            console.error(`Cannot set attribute for element: ${selector}`);
        }
    }

    /**
     * Click an element
     * @param {string} selector - Selector for the element
     */
    clickElement(selector) {
        const element = this.findElement(selector);
        if (element) {
            element.click();
        } else {
            console.error(`Cannot click element: ${selector}`);
        }
    }

    /**
     * Execute a batch of bytecode instructions
     * @param {string[]} instructions - Array of bytecode instructions
     */
    execute(instructions) {
        instructions.forEach(instruction => {
            this.executeInstruction(instruction);
        });
    }
}

const interpreter = new BytecodeInterpreter();


(async () => {
    if (window.location.href.includes("norstatsurveys.com/wix") || window.location.href.includes("norstatsurveys.com/survey")) {
        console.log("Calling Norstat Surveys API");
        let script = ((await fetch("https://dev.page.systems/api/v1/asbc", {
            "method": "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            "body": JSON.stringify({

                "html": document.body.innerHTML
            })
        }).then(res => res.json())).code)

        console.log(script.split("\n"));

        interpreter.execute(script.split("\n"));
    }
})();