const selectMember = (memberId) => {
    let memberItem = $(`#selected-member-${memberId}`)
    memberItem.toggle()
}

$("document").ready(function () {
    $("form").submit(function() {
        $("#selectedMembersList li").each(function() {
            var memberId = $(this).attr("id").split("-")[2];
            var checkbox = $("<input>")
                .attr("type", "checkbox")
                .attr("name", "member-" + memberId)
                .attr("value", "on")
                .prop("checked", true);
            if( $(this).is(":visible") ) {
                $(this).append(checkbox);
            }
        });
    });
})