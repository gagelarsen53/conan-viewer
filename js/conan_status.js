
$("#selector").load("selector.html", function(){
    $("#conan-package-selector").change(function(){
            $("#conan-content").load($(this).val(), function( response, status, xhr) {
            $("#conan-content table").addClass("table-bordered")
        })
    });
});

