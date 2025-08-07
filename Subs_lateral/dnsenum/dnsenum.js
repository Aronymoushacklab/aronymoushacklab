  const terminal = document.getElementById("terminal");
    const input = document.getElementById("input");

    // Define carpetas y sus enlaces
    const folders = [
      { name: "github", url: "https://github.com" },
      { name: "google", url: "https://google.com" },
      { name: "openai", url: "https://openai.com" },
      { name: "linux", url: "https://kernel.org" },
      { name: "linux", url: "https://kernel.org" },
      { name: "linux", url: "https://kernel.org" },
      { name: "linux", url: "https://kernel.org" },
    ];

    // Mantener el cursor al final
    function moveCaretToEnd(el) {
      el.focus();
      const range = document.createRange();
      range.selectNodeContents(el);
      range.collapse(false);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    }

    input.focus();

    document.addEventListener("click", () => {
      moveCaretToEnd(input);
    });

    input.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        const command = input.innerText.trim();
        processCommand(command);
      }
    });

    function processCommand(command) {
      const currentLine = terminal.lastElementChild;
      input.contentEditable = "false";

      const output = document.createElement("div");
      output.className = "output-line";

      if (command === "ls") {
        folders.forEach(folder => {
          const link = document.createElement("a");
          link.href = folder.url;
          link.textContent = folder.name;
          link.className = "folder-link";
          link.target = "_blank";
          output.appendChild(link);
        });
      } else if (command === "clear") {
        terminal.innerHTML = '';
        addNewPrompt();
        return;
      } else {
        output.textContent = `Command not found: ${command}`;
      }

      terminal.appendChild(output);
      addNewPrompt();
    }

    function addNewPrompt() {
      const line = document.createElement("div");
      const prompt = document.createElement("span");
      prompt.className = "prompt";
      prompt.textContent = "Aronymous@hacker:~$";

      const inputLine = document.createElement("span");
      inputLine.className = "input-line";
      inputLine.contentEditable = "true";
      inputLine.id = "input";

      const cursor = document.createElement("span");
      cursor.className = "blink";
      cursor.textContent = "_";

      line.appendChild(prompt);
      line.appendChild(document.createTextNode(" "));
      line.appendChild(inputLine);
      line.appendChild(cursor);

      terminal.appendChild(line);
      inputLine.focus();
      moveCaretToEnd(inputLine);

      // Remover evento antiguo y asignar nuevo
      inputLine.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          e.preventDefault();
          const command = inputLine.innerText.trim();
          processCommand(command);
        }
      });
    }