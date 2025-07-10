let a = "";
    let b = "";
    let op = "";
    let display = document.getElementById("display");

    function operatorClicked(symbol) {
      op = symbol;
      a = display.value;
      display.value = "";
    }

    function clearAll() {
      a = "";
      b = "";
      op = "";
      display.value = "";
    }

    function calculate() {
      b = display.value;

      let num1 = parseFloat(a);
      let num2 = parseFloat(b);
      let result = 0;

      if (op === "+") {
        result = num1 + num2;
      } else if (op === "-") {
        result = num1 - num2;
      } else if (op === "*") {
        result = num1 * num2;
      } else if (op === "/") {
        if (num2 === 0) {
          result = "Cannot divide by 0";
        } else {
          result = num1 / num2;
        }
      }

      display.value = result;
    }