// يدعم إضافة صور مرفقة ديناميكيًا حتى 20 صورة فقط في Inline
(function() {
    function updateAddButton() {
        var inlines = document.querySelectorAll('.dynamic-newsattachment_set');
        var addBtn = document.querySelector('.add-row a');
        if (inlines.length >= 20) {
            if (addBtn) addBtn.style.display = 'none';
            var msg = document.getElementById('max-attachments-msg');
            if (!msg) {
                var div = document.createElement('div');
                div.id = 'max-attachments-msg';
                div.className = 'text-danger fw-bold my-2';
                div.innerText = 'لا يمكن رفع أكثر من 20 صورة مرفقة لهذا الخبر.';
                var inlineGrp = document.querySelector('#newsattachment_set-group');
                if (inlineGrp) inlineGrp.appendChild(div);
            }
        } else {
            if (addBtn) addBtn.style.display = '';
            var msg = document.getElementById('max-attachments-msg');
            if (msg) msg.remove();
        }
    }
    document.addEventListener('DOMContentLoaded', function() {
        updateAddButton();
        document.body.addEventListener('click', function(e) {
            if (e.target.closest('.add-row a')) {
                setTimeout(updateAddButton, 100);
            }
        });
    });
})(); 