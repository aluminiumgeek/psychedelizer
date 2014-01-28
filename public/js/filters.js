
app.filter('remove_ext', function() {
    return function(text) {
        return text.substr(0, text.lastIndexOf('.'));
    };
})
