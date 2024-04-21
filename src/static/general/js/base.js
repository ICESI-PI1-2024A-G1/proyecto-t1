const DataTableInit = id => {
    let dataTable = $(`#${id}`).DataTable({
        "lengthMenu": [[5, 10, 25, -1], [5, 10, 25, "Todos"]],
        "pageLength":4,
        "language": {
            "url": "/static/general/json/datatables-ES.json"
        },
        // "searching": false,
        // dom: '<"table-wrapper"f>tip'
    });
    $(`#${id}Search`).on('input', function(){
        var searchText = $(this).val();
        console.log(dataTable.search("") === dataTable.search(searchText))
        dataTable.search(searchText).draw();

    })
    dataTable.on('draw.dt', function(){
        $(`#${id}Pagination`).append($('.dt-paging'));
        $(`#${id}Pagination`).append($('.dt-info'));
        $(".dt-paging").addClass("col-md-8")
        $(".dt-paging").css("overflow-x", "auto")
        $(".dt-info").addClass("col-md-4")
        $(".dt-search").parent().parent().hide()
    })
}
const showModal = (title, url) => {
    $.get(url, function (data) {
        $('#detailsContent').html(data);
        $('#detailsModal .modal-dialog').addClass('modal-lg');
        $('#detailsModal').modal('show');
        $('#detailsModalLabel').text(title);
    });
}