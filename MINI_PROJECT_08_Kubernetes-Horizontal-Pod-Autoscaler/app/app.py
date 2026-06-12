import time
import math
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

def simulate_heavy_load(duration=0.15):
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        _ = math.sqrt(math.sin(count) * math.cos(count) + 2.0)
        count += 1

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Calculator</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                --calc-bg: rgba(30, 41, 59, 0.45);
                --calc-border: rgba(255, 255, 255, 0.1);
                --display-bg: rgba(15, 23, 42, 0.6);
                --btn-bg: rgba(255, 255, 255, 0.05);
                --btn-hover: rgba(255, 255, 255, 0.12);
                --btn-active: rgba(255, 255, 255, 0.2);
                --accent-color: #8b5cf6;
                --accent-hover: #a78bfa;
                --text-primary: #f8fafc;
                --text-secondary: #94a3b8;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Outfit', sans-serif;
                background: var(--bg-gradient);
                color: var(--text-primary);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 1rem;
            }

            .calculator {
                background: var(--calc-bg);
                border: 1px solid var(--calc-border);
                border-radius: 24px;
                padding: 24px;
                width: 100%;
                max-width: 380px;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            }

            .display {
                background: var(--display-bg);
                border: 1px solid var(--calc-border);
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 24px;
                text-align: right;
                min-height: 90px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                overflow: hidden;
            }

            .display-history {
                font-size: 0.95rem;
                color: var(--text-secondary);
                min-height: 20px;
                word-wrap: break-word;
                word-break: break-all;
            }

            .display-input {
                font-size: 2.2rem;
                font-weight: 600;
                overflow-x: auto;
                white-space: nowrap;
                margin-top: 5px;
            }

            .display-input::-webkit-scrollbar {
                height: 4px;
            }

            .display-input::-webkit-scrollbar-thumb {
                background: rgba(255,255,255,0.2);
                border-radius: 2px;
            }

            .buttons-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
            }

            button {
                border: none;
                background: var(--btn-bg);
                color: var(--text-primary);
                font-family: 'Outfit', sans-serif;
                font-size: 1.35rem;
                font-weight: 600;
                padding: 18px 0;
                border-radius: 14px;
                cursor: pointer;
                transition: all 0.2s ease;
                border: 1px solid rgba(255, 255, 255, 0.02);
            }

            button:hover {
                background: var(--btn-hover);
                transform: translateY(-2px);
            }

            button:active {
                background: var(--btn-active);
                transform: translateY(0);
            }

            button.operator {
                color: #a78bfa;
                background: rgba(139, 92, 246, 0.1);
            }

            button.operator:hover {
                background: rgba(139, 92, 246, 0.2);
            }

            button.clear {
                color: #f87171;
                background: rgba(248, 113, 113, 0.1);
            }

            button.clear:hover {
                background: rgba(248, 113, 113, 0.2);
            }

            button.equals {
                grid-column: span 2;
                background: var(--accent-color);
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
            }

            button.equals:hover {
                background: var(--accent-hover);
                box-shadow: 0 6px 16px rgba(139, 92, 246, 0.45);
            }

            .loading-indicator {
                font-size: 0.8rem;
                color: var(--accent-hover);
                opacity: 0;
                transition: opacity 0.2s ease;
                text-align: left;
            }

            .loading-indicator.show {
                opacity: 1;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <div class="display">
                <div class="display-history" id="history"></div>
                <div class="display-input" id="input">0</div>
                <div class="loading-indicator" id="loading">Calculating...</div>
            </div>
            <div class="buttons-grid">
                <button class="clear" onclick="clearDisplay()">C</button>
                <button class="operator" onclick="setOperator('divide')">/</button>
                <button class="operator" onclick="setOperator('multiply')">*</button>
                <button class="operator" onclick="setOperator('subtract')">-</button>

                <button onclick="appendNumber('7')">7</button>
                <button onclick="appendNumber('8')">8</button>
                <button onclick="appendNumber('9')">9</button>
                <button class="operator" onclick="setOperator('add')">+</button>

                <button onclick="appendNumber('4')">4</button>
                <button onclick="appendNumber('5')">5</button>
                <button onclick="appendNumber('6')">6</button>
                <button onclick="appendNumber('.')">.</button>

                <button onclick="appendNumber('1')">1</button>
                <button onclick="appendNumber('2')">2</button>
                <button onclick="appendNumber('3')">3</button>
                <button onclick="appendNumber('0')">0</button>

                <button class="equals" onclick="performCalculation()">=</button>
            </div>
        </div>

        <script>
            let currentInput = '';
            let previousInput = '';
            let activeOperator = null;

            const inputEl = document.getElementById('input');
            const historyEl = document.getElementById('history');
            const loadingEl = document.getElementById('loading');

            function updateDisplay() {
                inputEl.innerText = currentInput || '0';
                if (activeOperator) {
                    const opSymbol = { 'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/' }[activeOperator];
                    historyEl.innerText = `${previousInput} ${opSymbol}`;
                } else {
                    historyEl.innerText = '';
                }
            }

            function appendNumber(num) {
                if (num === '.' && currentInput.includes('.')) return;
                currentInput += num;
                updateDisplay();
            }

            function clearDisplay() {
                currentInput = '';
                previousInput = '';
                activeOperator = null;
                updateDisplay();
            }

            function setOperator(op) {
                if (currentInput === '' && previousInput === '') return;
                if (currentInput !== '') {
                    if (previousInput !== '' && activeOperator) {
                        // Compute middle result
                        performCalculation();
                    } else {
                        previousInput = currentInput;
                        currentInput = '';
                    }
                }
                activeOperator = op;
                updateDisplay();
            }

            function performCalculation() {
                if (!activeOperator || previousInput === '' || currentInput === '') return;
                
                loadingEl.classList.add('show');
                const url = `/calculate?op=${activeOperator}&a=${previousInput}&b=${currentInput}`;
                
                fetch(url)
                    .then(res => res.json())
                    .then(data => {
                        loadingEl.classList.remove('show');
                        if (data.error) {
                            inputEl.innerText = 'Error';
                            currentInput = '';
                        } else {
                            currentInput = data.result.toString();
                        }
                        previousInput = '';
                        activeOperator = null;
                        updateDisplay();
                    })
                    .catch(err => {
                        loadingEl.classList.remove('remove');
                        inputEl.innerText = 'Error';
                        currentInput = '';
                        updateDisplay();
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/calculate', methods=['GET'])
def calculate():
    operation = request.args.get('op', 'add')
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return jsonify({"error": "Invalid numbers"}), 400

    # Simulate CPU-heavy processing for testing HPA scaling
    simulate_heavy_load()

    result = 0
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return jsonify({"error": "Division by zero"}), 400
        result = a / b
    else:
        return jsonify({"error": f"Unknown operation: {operation}"}), 400

    return jsonify({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
