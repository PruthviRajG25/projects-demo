

        let display = document.getElementById('display');
        let currentInput = '';
        let operator = '';
        let previousInput = '';
        let shouldResetDisplay = false;

        function appendToDisplay(value) {
            if (shouldResetDisplay) {
                display.value = '';
                shouldResetDisplay = false;
            }

            if (['+', '-', '*', '/','%'].includes(value)) {
                if (currentInput !== '') {
                    if (previousInput !== '' && operator !== '') {
                        calculate();
                    }
                    previousInput = currentInput;
                    operator = value;
                    currentInput = '';
                    display.value = previousInput + ' ' + getOperatorSymbol(value) + ' ';
                }
            } else {
                currentInput += value;
                if (operator !== '') {
                    display.value = previousInput + ' ' + getOperatorSymbol(operator) + ' ' + currentInput;
                } else {
                    display.value = currentInput;
                }
            }
        }

        function getOperatorSymbol(op) {
            switch(op) {
                case '+': return '+';
                case '-': return '-';
                case '*': return '×';
                case '/': return '÷';
                case '%':return '%';
                default: return op;
            }
        }

        function calculate() {
            if (previousInput !== '' && currentInput !== '' && operator !== '') {
                try {
                    let result = eval(previousInput + operator + currentInput);
                    result = Math.round(result * 100000000) / 100000000; // Handle floating point precision
                    display.value = result;
                    previousInput = result.toString();
                    currentInput = '';
                    operator = '';
                    shouldResetDisplay = true;
                } catch (error) {
                    display.value = 'Error';
                    clearAll();
                }
            }
        }

        function clearDisplay() {
            clearAll();
            display.value = '0';
        }

        function clearAll() {
            currentInput = '';
            operator = '';
            previousInput = '';
            shouldResetDisplay = false;
        }

        function deleteLast() {
            if (currentInput !== '') {
                currentInput = currentInput.slice(0, -1);
                if (operator !== '') {
                    display.value = previousInput + ' ' + getOperatorSymbol(operator) + ' ' + currentInput;
                } else {
                    display.value = currentInput || '0';
                }
            } else if (operator !== '') {
                operator = '';
                currentInput = previousInput;
                previousInput = '';
                display.value = currentInput;
            }
        }

        // Keyboard support
        document.addEventListener('keydown', function(event) {
            const key = event.key;
            
            if ('0123456789.'.includes(key)) {
                appendToDisplay(key);
            } else if ('+-*/'.includes(key)) {
                appendToDisplay(key);
            } else if (key === 'Enter' || key === '=') {
                event.preventDefault();
                calculate();
            } else if (key === 'Escape') {
                clearDisplay();
            } else if (key === 'Backspace') {
                event.preventDefault();
                deleteLast();
            }
        });

        // Initialize display
        display.value = '0';
    