// Main JavaScript for Medicine Recommendation System

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    
    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })
    
    // Symptom form validation
    const symptomForm = document.querySelector('form[action="/symptoms"]');
    if (symptomForm) {
        symptomForm.addEventListener('submit', function(event) {
            const selectedSymptoms = document.querySelectorAll('input[name="symptoms"]:checked');
            if (selectedSymptoms.length === 0) {
                event.preventDefault();
                alert('Please select at least one symptom');
            }
        });
    }
    
    // Search functionality for symptoms
    const symptomSearch = document.getElementById('symptomSearch');
    if (symptomSearch) {
        symptomSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const symptomCheckboxes = document.querySelectorAll('.symptom-checkbox');
            
            symptomCheckboxes.forEach(function(checkbox) {
                const symptomName = checkbox.querySelector('label').textContent.toLowerCase();
                if (symptomName.includes(searchTerm)) {
                    checkbox.style.display = '';
                } else {
                    checkbox.style.display = 'none';
                }
            });
        });
    }
    
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert:not(.alert-permanent)');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.classList.add('fade');
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 5000);
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
});