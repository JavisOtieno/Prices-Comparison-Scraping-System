$(function(e) {
    "use strict";

    //______Basic Data Table
    $('#basic-datatable').DataTable({
        language: {
            searchPlaceholder: 'Search...',
            sSearch: '',
        }
    });


    // $('#responsive-datatable').DataTable({
    //     "order": [0, 'desc'],
    //     language: {
    //         searchPlaceholder: 'Search...',
    //         scrollX: "100%",
    //         sSearch: '',
    //     }
    // });

       //______Basic Data Table
       var table2=$('#responsive-datatable').DataTable({
        "order": [0, 'desc'],
        'ordering': true,
        language: {
            searchPlaceholder: 'Search...',
            scrollX: "100%",
            sSearch: '',
        
        },
        buttons: [
            {
                extend: 'copy',
                title: 'FAVEExport',
                exportOptions: {
                    columns: function(idx, data, node) {
                        // Prevent export of columns with certain IDs
                        var columnId = $(node).attr('id');
                        return columnId !== 'map-column' && columnId !== 'view-column' &&columnId !== 'edit-column' && columnId !== 'delete-column';
                    },
                    format: {
                        body: function (data, row, column, node) {
                            return data.replace(/\n/g, '\r\n'); // Replace \n with \r\n for clipboard copy
                        }
                    }
                }
            }
            , 
        {
            extend: 'excelHtml5',
            title: 'FAVEExport',
            exportOptions: {
                columns: function(idx, data, node) {
                    // Prevent export of columns with certain IDs
                    var columnId = $(node).attr('id');
                    return columnId !== 'map-column' && columnId !== 'view-column' && columnId !== 'edit-column' && columnId !== 'delete-column';
                },
                format: {
                    body: function (data, row, column, node) {
                        return data.replace(/\n/g, '\r\n'); // Replace \n with \r\n for Excel
                    }
                }
            }
        }
        
        , 
        {
            extend: 'pdf',
            title: 'FAVEExport',
            exportOptions: {
                columns: function(idx, data, node) {
                    // Prevent export of columns with certain IDs
                    var columnId = $(node).attr('id');
                    return columnId !== 'map-column' && columnId !== 'view-column' &&columnId !== 'edit-column' && columnId !== 'delete-column';
                },
                format: {
                    body: function (data, row, column, node) {
                        return data.replace(/\n/g, '\n'); // Preserve newlines for PDF
                    }
                }
            },
            
        },
        
        ,         {
            extend: 'colvis',
            title: 'FAVEExport',
            // columns: function(idx, data, node) {
            //         // Prevent export of columns with certain IDs
            //         var columnId = $(node).attr('id');
            //         return columnId !== 'edit-column' && columnId !== 'delete-column';
            //     }
            
        }
    ],
        
    });

    //______File-Export Data Table
    var table = $('#file-datatable').DataTable({
        buttons: ['copy', 'excel', 'pdf', 'colvis'],
        language: {
            searchPlaceholder: 'Search...',
            scrollX: "100%",
            sSearch: '',
        }
    });
    table.buttons().container()
        .appendTo('#file-datatable_wrapper .col-md-6:eq(0)');

    //______Delete Data Table
    var table = $('#delete-datatable').DataTable({
        language: {
            searchPlaceholder: 'Search...',
            sSearch: '',
        }
    });
    $('#delete-datatable tbody').on('click', 'tr', function() {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
    $('#button').on('click', function() {
        table.row('.selected').remove().draw(false);
    });
    $('#example3').DataTable( {
        responsive: {
            details: {
                display: $.fn.dataTable.Responsive.display.modal( {
                    header: function ( row ) {
                        var data = row.data();
                        return 'Details for '+data[0]+' '+data[1];
                    }
                } ),
                renderer: $.fn.dataTable.Responsive.renderer.tableAll( {
                    tableClass: 'table'
                } )
            }
        }
    } );
    $('#example2').DataTable({
		responsive: true,
		language: {
			searchPlaceholder: 'Search...',
			sSearch: '',
			lengthMenu: '_MENU_ items/page',
		}
	});
	

    //______Select2 
    $('.select2').select2({
        minimumResultsForSearch: Infinity
    });

});