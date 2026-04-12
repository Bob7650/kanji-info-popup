document.addEventListener("DOMContentLoaded", onReady);

let kdpopover = undefined;
let visible = false;
let oldSelection = "";

function onReady() {
    initPopover();
    document.body.appendChild(kdpopover);
    document.addEventListener("mouseup", onMouseUp);
}

function onMouseUp(e) {
    if (visible && isInsidePopover(e.clientX, e.clientY)) {
        console.log("Mouse inside popover, canceling event");
        return;
    }

    const selection = getSelectionText();

    if (!selection) {
        hidePopover();
        return;
    }

    setPopoverContent(selection);
}

function setPopoverContent(content) {
    const command = "KanjiPopupContentPrep:" + content;
    pycmd(command, (kanjiDataList) => {
        if (kanjiDataList.length == 0) return;
        buildPopover(kanjiDataList);
        showPopover(10, 10);
    });
}

function initPopover() {
    kdpopover = document.createElement("div");
    kdpopover.id = "kdpover";

    kdpopover.style.display = visible ? "flex" : "none";
}

function buildPopover(kanjiDataList) {
    kdpopover.innerHTML = "";

    for (let i = 0; i < kanjiDataList.length; i++) {
        kanjiData = kanjiDataList[i];
        kdpopover.appendChild(buildKanjiEntry(kanjiData));
        if (i != kanjiDataList.length - 1)
            kdpopover.appendChild(document.createElement("hr"));
    }
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

function hidePopover() {
    kdpopover.style.display = "none";
    visible = false;
}

function showPopover(x, y) {
    kdpopover.style.left = `${x}px`;
    kdpopover.style.top = `${y}px`;
    kdpopover.style.display = "flex";
    visible = true;
}

function getSelectionText() {
    let text = "";

    if (window.getSelection()) {
        text = window.getSelection().toString();
    }

    return text;
}

function isInsidePopover(x, y) {
    const popoverRect = kdpopover.getBoundingClientRect();

    // temporary solution to make interaction with scrollbar not close the popover
    const scrollbarPadding = 15;

    return (
        popoverRect.x < x &&
        x < popoverRect.width + scrollbarPadding &&
        popoverRect.y < y &&
        y < popoverRect.height
    );
}
