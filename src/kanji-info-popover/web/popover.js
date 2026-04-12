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
        //console.log("Mouse inside popover, canceling event");
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
    pycmd(command, (displayData) => {
        if (displayData["kanjiDataList"].length === 0) return;
        if (displayData["displayConfig"].length === 0) return;
        buildPopover(displayData);
        showPopover(10, 10);
    });
}

function initPopover() {
    kdpopover = document.createElement("div");
    kdpopover.id = "kdpover";

    kdpopover.style.display = visible ? "flex" : "none";
}

function buildPopover(displayData) {
    kanjiDataList = displayData["kanjiDataList"];
    displayConfig = displayData["displayConfig"];
    kdpopover.innerHTML = "";

    for (let i = 0; i < kanjiDataList.length; i++) {
        kanjiData = kanjiDataList[i];
        kdpopover.appendChild(buildKanjiEntry(kanjiData, displayConfig));
        if (i != kanjiDataList.length - 1)
            kdpopover.appendChild(document.createElement("hr"));
    }
}

function buildKanjiEntry(kanjiData, displayConfig) {
    const kanjiEntry = document.createElement("div");

    if (displayConfig["displayKanji"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Kanji</span><span class="kdpover-kanji" id="kdpover-kanji">${kanjiData.kanji}</span>`;
    if (displayConfig["displayMeanings"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Meaning</span><span class="kdpover-content" id="kdpover-meanings">${kanjiData.meanings.join(", ")}</span>`;
    if (displayConfig["displayOnyomi"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Onyomi</span><span class="kdpover-content" id="kdpover-onyomi">${kanjiData.on_readings.join(", ")}</span>`;
    if (displayConfig["displayKunyomi"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Kunyomi</span><span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.kun_readings.join(", ")}</span>`;
    if (displayConfig["displayStrokeCount"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Stroke Count</span><span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.stroke_count}</span>`;
    if (displayConfig["displayJLPT"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">JLPT</span><span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.jlpt}</span>`;
    if (displayConfig["displayGrade"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Grade</span><span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.grade}</span>`;
    if (displayConfig["displayHeisig"])
        kanjiEntry.innerHTML += `<span class="kdpover-header">Heisig English</span><span class="kdpover-content" id="kdpover-kunyomi">${kanjiData.heisig_en}</span>`;

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
