const selectMember = (memberId) => {
    let memberItem = $(`#selected-member-${memberId}`)
    memberItem.toggle()
}        