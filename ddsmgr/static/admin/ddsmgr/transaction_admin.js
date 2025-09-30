(function(){
    // после загрузки DOM
    function qs(sel) { return document.querySelector(sel); }
    function qsa(sel) { return document.querySelectorAll(sel); }

    function init() {
        var category = qs('#id_category');
        var subcategory = qs('#id_subcategory');

        if (!category || !subcategory) return;

        function clearOptions() {
            subcategory.innerHTML = '';
        }

        function addOption(value, text, selected) {
            var opt = document.createElement('option');
            opt.value = value;
            opt.text = text;
            if (selected) opt.selected = true;
            subcategory.appendChild(opt);
        }

        function loadSubcats(catId, selectedId) {
            clearOptions();
            if (!catId) {
                addOption('', '---------');
                return;
            }
            var url = window.location.pathname.replace(/\/$/, '') + 'get_subcategories/?category=' + encodeURIComponent(catId);
            // note: uses relative admin url handled by admin view
            fetch(url, {credentials: 'same-origin'}).then(function(resp){
                return resp.json();
            }).then(function(data){
                addOption('', '---------');
                data.results.forEach(function(r){
                    addOption(r.id, r.name, String(r.id) === String(selectedId));
                });
            }).catch(function(err){
                console.error('Failed to load subcategories', err);
            });
        }

        // при изменении категории — перезагрузить подкатегории
        category.addEventListener('change', function(e){
            loadSubcats(e.target.value, null);
        });

        // при загрузке формы (на редактировании) — подгрузим подкатегории и отметим выбранную
        var initialCategory = category.value;
        var initialSubcat = subcategory.getAttribute('data-initial') || subcategory.value;
        if (initialCategory) {
            loadSubcats(initialCategory, initialSubcat);
        }
    }

    // DOMContentLoaded в админке иногда уже загружен
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
