document.addEventListener("DOMContentLoaded", onReady);

const kdpopover = document.createElement("div");
const dragHandle = document.createElement("div");
const dataSection = document.createElement("div");

let anchor = {x: 10, y: 100};
let offsetVector = { x: 0, y: 0 }

let visible = false;
let isDragged = false;
let oldSelection = "";

function onReady() {
    initPopover();
    document.body.appendChild(kdpopover);
    document.addEventListener("mouseup", onMouseUp);
    document.addEventListener("mousemove", onMouseMove);
}

function onMouseUp(e) {
    setTimeout(updatePopover, 100, e);
}

function onMouseMove(e){
    if(isDragged){
        anchor.x = e.clientX + offsetVector.x;
        anchor.y = e.clientY + offsetVector.y;
        showPopover();
    }
}

function updatePopover(e){
    if (isInsidePopover(e.clientX, e.clientY)) return;
    
    const selection = getSelectionText();

    if (visible) {
        hidePopover(); 
    }

    if (selection) {
        requestPopoverData(selection);
    }
}

function requestPopoverData(content) {
    const command = "KanjiPopupContentPrep:" + content;
    pycmd(command, onDataReceived);
}

function onDataReceived(displayData) {
    if (displayData["kanjiDataList"].length === 0) return;
    if (displayData["displayConfig"].length === 0) return;
    buildPopover(displayData);
    showPopover();
}

function initPopover() {
    kdpopover.id = "kdpover";
    kdpopover.style.display = visible ? "flex" : "none";

    dragHandle.id = "dragHandle";
    dragHandle.innerHTML = "<p>⠿</p>";
    dragHandle.addEventListener("mousedown", onPopoverDragStart)
    dragHandle.addEventListener("mouseup", onPopoverDragEnd)

    dataSection.id = "dataSection";

    kdpopover.appendChild(dragHandle);
    kdpopover.appendChild(dataSection)
}

function onPopoverDragStart(e){
    offsetVector.x = anchor.x - e.clientX;
    offsetVector.y = anchor.y - e.clientY;
    isDragged = true;
    e.stopPropagation();
}

function onPopoverDragEnd(e){
    isDragged = false;
    e.stopPropagation();
}

function buildPopover(displayData) {
    kanjiDataList = displayData["kanjiDataList"];
    displayConfig = displayData["displayConfig"];

    dataSection.innerHTML = "";

    for (let i = 0; i < kanjiDataList.length; i++) {
        kanjiData = kanjiDataList[i];
        dataSection.appendChild(buildKanjiEntry(kanjiData, displayConfig));
        if (i != kanjiDataList.length - 1)
            dataSection.appendChild(document.createElement("hr"));
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

function showPopover() {
    kdpopover.style.left = `${anchor.x}px`;
    kdpopover.style.top = `${anchor.y}px`;
    kdpopover.style.display = "flex";
    visible = true;
}

function getSelectionText() {
    let text = "";

    if (window.getSelection()) {
        text = window.getSelection().toString();
        text = text.trim();
    }
    return text;
}

function isInsidePopover(x, y) {
    const popoverRect = kdpopover.getBoundingClientRect();

    // to make interaction with scrollbar not close the popover
    const scrollbarPadding = 15;

    return (
        popoverRect.x < x &&
        x < popoverRect.width + scrollbarPadding &&
        popoverRect.y < y &&
        y < popoverRect.height
    );
}
