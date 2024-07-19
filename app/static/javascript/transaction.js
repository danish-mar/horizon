$(document).ready(function() {
    // Show loading indicator initially with fade in
    $('#loading-container').fadeIn();

    fetch('/transactions')
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator with fade out
            $('#loading-container').fadeOut(() => {
                $('#transactions-list').show(); // Show transactions list

                if (data.transactions) {
                    const transactionsList = $('#transactions-list');

                    // Sort transactions by created_at date in descending order
                    data.transactions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

                    data.transactions.forEach(transaction => {
                        const transactionTypeClass = transaction.transaction_type === 'credit' ? 'transaction-credit' : 'transaction-debit';
                        const transactionIcon = transaction.transaction_type === 'credit' ? 'fa-arrow-down' : 'fa-arrow-up';
                        const accountNumber = transaction.transaction_type === 'credit' ? transaction.from_account : transaction.to_account;
                        const formattedAccountNumber = accountNumber ? `******${accountNumber.slice(-4)}` : 'N/A';

                        // Determine platform icon dynamically
                        let platformIcon;
                        switch(transaction.platform) {
                            case 'Internet Banking':
                                platformIcon = 'fa-globe';
                                break;
                            case 'NPI':
                                platformIcon = 'fa-mobile-alt';
                                break;
                            case 'Card':
                                platformIcon = 'fa-credit-card';
                                break;
                            default:
                                platformIcon = 'fa-question';
                        }

                        const transactionItem = `
                            <li class="list-group-item bg-dark text-light border-0 transaction-item"
                                data-id="${transaction.transaction_id}"
                                data-description="${transaction.description.toLowerCase()}"
                                data-type="${transaction.transaction_type}"
                                data-amount="${transaction.amount}"
                                data-date="${transaction.created_at}"
                                data-from-account="${transaction.from_account || ''}"
                                data-to-account="${transaction.to_account || ''}"
                                onclick="openTransactionPage(${transaction.transaction_id})">
                                <i class="fas ${transactionIcon} ${transactionTypeClass}"></i>
                                <span class="font-weight-bold"> ${formattedAccountNumber} </span>
                                <span class="float-end ${transactionTypeClass}">${transaction.amount} $</span>
                                <br>
                                <small>${new Date(transaction.created_at).toLocaleString()}</small>
                                <br>
                                <small>${transaction.description}</small>
                                <i class="fas ${platformIcon} float-end"></i>
                            </li>
                        `;
                        transactionsList.append(transactionItem);
                        // Animate newly added transaction
                        transactionsList.find('.transaction-item').last().hide().fadeIn('slow');
                    });

                    // Add click event listener to all transaction items
                    $('.transaction-item').on('click', function () {
                        const transactionId = $(this).data('id');
                        openTransactionPage(transactionId);
                    });
                } else {
                    $('#transactions-list').append('<li class="list-group-item bg-dark text-light border-0">No transactions found</li>');
                }
            });
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
            $('#loading-container').fadeOut(); // Hide loading GIF on error
            $('#transactions-list').append('<li class="list-group-item bg-dark text-light border-0">Error loading transactions</li>');
        });

    // Filter transactions based on search input and filters
    $('#search-bar, #account-filter, #type-filter').on('input change', function() {
        const searchQuery = $('#search-bar').val().toLowerCase();
        const accountFilter = $('#account-filter').val();
        const typeFilter = $('#type-filter').val();

        $('.transaction-item').each(function() {
            const description = $(this).data('description') || '';
            const fromAccount = $(this).data('from-account') || '';
            const toAccount = $(this).data('to-account') || '';
            const type = $(this).data('type') || '';
            const amount = $(this).data('amount') || '';
            const date = $(this).data('date') || '';
            const lastAccountNumber = ((fromAccount || toAccount) + '').slice(-4);

            const matchesSearch = description.includes(searchQuery) || date.includes(searchQuery) || amount.toString().includes(searchQuery) || lastAccountNumber.includes(searchQuery);
            const matchesAccount = (accountFilter === '' || (accountFilter === 'from_account' && fromAccount) || (accountFilter === 'to_account' && toAccount));
            const matchesType = (typeFilter === '' || typeFilter === type);

            if (matchesSearch && matchesAccount && matchesType) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Toggle filter dropdown
    $('#filter-btn').on('click', function() {
        $('#filter-dropdown').toggle();
    });

    // Close dropdown when clicking outside
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.search-container').length) {
            $('#filter-dropdown').hide();
        }
    });
});

// Function to open transaction page
function openTransactionPage(transactionId) {
    const url = `/transactions/${transactionId}`;
    window.open(url, '_blank');
}
