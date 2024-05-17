const DataTableInit = (id, pageLength=4, columnDefs=[]) => {
    let dataTable = $(`#${id}`).DataTable({
        "lengthMenu": [[5, 10, 25, -1], [5, 10, 25, "Todos"]],
        "pageLength":pageLength,
        // "language": {
        //     "url": "/static/general/json/datatables-ES.json"
        // },
        "columnDefs": columnDefs,
        // "searching": false,
        // dom: '<"table-wrapper"f>tip'
    });

    $(`#${id}Search`).on('input', function(){
        var searchText = $(this).val();
        dataTable.search(searchText).draw();
    })
    dataTable.on('draw.dt', function(){
        $(`#${id}Pagination`).append($(`#${id}_wrapper .dt-paging`));
        $(`#${id}Pagination`).append($(`#${id}_wrapper .dt-info`));
        $(".dt-paging").addClass("col-md-8")
        $(".dt-paging").css("overflow-x", "auto")
        $(".dt-info").addClass("col-md-4")
        $(".dt-search").parent().parent().hide()
        setCardHeight()
    })
    dataTable.draw();
}

const setCardHeight = () => {
    var newHeight = $(window).height();
    newHeight -= $('#navBarHeader').outerHeight();
    newHeight -= $('.card-header').outerHeight();
    newHeight -= $('.card-footer').outerHeight();
    var htmlFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
    var marginInPixels = 1.5 * htmlFontSize;
    $(".card-fluid").height(newHeight-marginInPixels*2)
}

$(window).on("load", setCardHeight)
$(window).on("resize", setCardHeight)

const showModal = (title, url, size="") => {
    console.log("Mostrando modal")
    $.get(url, function (data) {
        $('#detailsContent').html(data);
        $('#detailsModal .modal-dialog').removeClass().addClass('modal-dialog');
        $('#detailsModal .modal-dialog').css('max-width', '');
        if(size) {
            console.log("Agregando clase: ", `modal-${size}`)
            $('#detailsModal .modal-dialog').addClass(`modal-${size}`)
            if(size === 'xxl') {
                $('#detailsModal .modal-dialog').css('max-width', '90%');
            }
        } else {
            $('#detailsModal .modal-dialog').addClass('modal-lg');
        }
        $('#detailsModal').modal('show');
        $('#detailsModalLabel').text(title);
    });
}

$(document).ready(function() {
    $('#detailsModal').on('hidden.bs.modal', function () {
        console.log("Modal cerrado")
        $("#detailsModal .modal-dialog").removeClass('modal-sm modal-xl');
    });
});