
function calculatePoint(i, intervalSize, colorRangeInfo){
    var {colorStart, colorEnd, useEndAsStart} = colorRangeInfo;

    return (useEndAsStart ? (colorEnd - (i * intervalSize)): (colorStart + (i * intervalSize)))

}

function interpolateColors(dataLength, colorScale, colorRangeInfo){
    var {colorStart, colorEnd} = colorRangeInfo;
    var colorRange = colorEnd - colorStart
    var intervalSize = colorRange / dataLength
    var i, colorPoint;
    var colorArray = [];

    for (i=0; i< dataLength; i++){
        colorPoint = calculatePoint(i, intervalSize, colorRangeInfo);
        colorArray.push(colorScale(colorPoint));
    }

    return colorArray;
}