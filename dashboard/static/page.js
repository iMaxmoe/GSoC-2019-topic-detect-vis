// Sidebar toggle
$(document).ready(function() {
    $(".sidebar.menu").sidebar("attach events", ".toggler"), 
    $(window).resize(function() {$(".ui.sidebar").sidebar("hide")}),
    $(".ui.dropdown").dropdown(),
    $(".spoiler").hide(),
    $("#aboutModal").modal("attach events", ".aboutTriggerer", "show"),
    $("#shareModal").modal("attach events", ".shareTriggerer", "show"),
    $("#friendsModal").modal("attach events", ".friendsTriggerer", "show"),
    $("#copyButton").popup({on: "click"}),
    $("#copyButton").click(function() {$("#siteUrl").select(), document.execCommand("copy")});
});