document.addEventListener("DOMContentLoaded", onReady);

let kdpopover = undefined;
let timeoutId;

function onReady() {
    initPopover();
    document.body.appendChild(kdpopover);
    document.addEventListener("mouseup", onMouseUp);
}

function onMouseUp(e) {
    const selection = getSelectionText();

    if (!selection) {
        hidePopover();
        return;
    }

    setPopoverContent(selection);
}

function setPopoverContent(content) {
    const command = "KanjiPopupContentPrep:" + content;
    console.log(`Sending command to python cmd ${command}`);
    pycmd(command, (kanjiListJson) => {
        console.log(`Received ${kanjiListJson}`);
        //kanjiList = JSON.parse(kanjiListJson);
        buildPopover(kanjiListJson);
        showPopover(10, 10);
    });
}

function initPopover() {
    kdpopover = document.createElement("div");
    kdpopover.id = "kdpover";
}

function buildPopover(kanjiDataList) {
    kdpopover.innerHTML = "";
    kanjiDataList.forEach((kanjiData) => {
        kdpopover.appendChild(buildKanjiEntry(kanjiData));
        kdpopover.appendChild(document.createElement("hr"));
    });
}

function buildKanjiEntry(kanjiData) {
    const kanjiEntry = document.createElement("div");

    kanjiEntry.innerHTML = `<span class="kdpover-header">Kanji</span>
    <span class="kdpover-kanji" id="kdpover-kanji">${kanjiData.kanji}</span>
    <span class="kdpover-header">Meaning</span>
    <span class="kdpover-content" id="kdpover-meanings">${kanjiData.meanings.join(", ")}</span>
    <span class="kdpover-header">Onyomi</span>
    <span class="kdpover-content" id="kdpover-onyomi">${kanjiData.on_readings.join(", ")}</span>
    <span class="kdpover-header">Kunyomi</span>
    <span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.kun_readings.join(", ")}</span>
    `;

    return kanjiEntry;
}

// function requestHidePopover() {
//     timeoutId = window.setTimeout(() => hidePopover(), 200);
// }

// function cancelHidePopover() {
//     window.clearTimeout(timeoutId);
// }

function hidePopover() {
    kdpopover.style.display = "none";
}

function showPopover(x, y) {
    kdpopover.style.left = `${x}px`;
    kdpopover.style.top = `${y}px`;
    kdpopover.style.display = "flex";
}

function getSelectionText() {
    let text = "";

    if (window.getSelection()) {
        text = window.getSelection().toString();
    }

    return text;
}
