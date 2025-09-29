let boxes = document.querySelectorAll(".box");
let resetBtn = document.querySelector("#reset-btn");
let newGameBtn = document.querySelector("#new-btn");
let msgContainer = document.querySelector(".msg-container")
let msg = document.querySelector("#msg")

let turnO = true;
const winPatterns = [[0, 1, 2], [0, 3, 6], [0, 4, 8], [1, 4, 7], [2, 5, 8], [2, 4, 6], [3, 4, 5], [6, 7, 8]];


boxes.forEach((box) => {
    box.addEventListener("click", () => {
        // console.log("click");
        if (turnO) {
            box.innerText = "O";
            turnO = false;

        }
        else {
            box.innerText = "X";
            turnO = true;
        }
        box.disabled = true;

        checkWinner();
    })
})
const disableBoxes = () => {
    for (let box of boxes) {
        box.disabled = true
    }
}
const enableBoxes = () => {
    for (let box of boxes) {
        box.disabled = false;
        box.innerText = "";

    }
}

const resetGame = () => {
    turnO = true;
    enableBoxes();
    msgContainer.classList.add("hide");
}


const showWinner = (winner) => {
    msg.innerHTML = `You are Winner  ${winner}`;
    msgContainer.classList.remove("hide");
    disableBoxes();

}

const checkWinner = () => {
    let winnerFound = false;
    for (let pattern of winPatterns) {
        let posVal1 = boxes[pattern[0]].innerText;
        let posVal2 = boxes[pattern[1]].innerText;
        let posVal3 = boxes[pattern[2]].innerText;
        if (posVal1 !== "" && posVal1 === posVal2 && posVal2 === posVal3) {
            showWinner(posVal1);
            winnerFound = true;
            break;
        }
    }
    // Check for draw
    if (!winnerFound) {
        let filledBoxes = 0;
        boxes.forEach(box => {
            if (box.innerText !== "") filledBoxes++;
        });
        if (filledBoxes === boxes.length) {
            msg.innerHTML = "Game Draw!";
            msgContainer.classList.remove("hide");
            disableBoxes();
        }
    }
}

newGameBtn.addEventListener("click", resetGame);
resetBtn.addEventListener("click", resetGame);
