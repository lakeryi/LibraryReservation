$(function() {

    $("section.contact-w3ls input,section.contact-w3ls textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // something to have when submit produces an error ?
            // Not decided if I need it yet
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var ID = $("section.contact-w3ls input#ID").val();
            var psw = $("section.contact-w3ls input#psw").val();
            var email = $("section.contact-w3ls input#email").val();
            var message = $("section.contact-w3ls textarea#message").val();
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
    $('#success').html('');
});
