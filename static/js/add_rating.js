// Define the CSRF token variable obtained from the template
var csrfToken = "{{ csrf_token }}";

var listComments = []

// Function to truncate the cookie string to the first 5 characters and last 4 characters
function truncateCookie(cookie) {
    if (cookie.length > 9) {
        return cookie.substr(0, 5) + '...' + cookie.substr(-4);
    }
    return cookie; // If the cookie length is less than or equal to 9, no truncation needed
}

// Function to add a new row to the data table
function addRowToTable(cookie, username, password) {
    const truncatedCookie = truncateCookie(cookie);
    const tableBody = document.getElementById("data-table-body");
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
             <td>${truncatedCookie}</td>
             <td>${username}</td>
             <td class="password-cell">******</td>
             <td>
                 <button class="btn btn-danger btn-sm remove-button">Remove</button>
             </td>
         `;
    // Store the actual password value as a custom data attribute
    newRow.dataset.passwordValue = password;
    newRow.dataset.fullCookie = cookie;
    tableBody.appendChild(newRow);
}

// Function to reset input fields
function resetInputFields() {
    document.getElementById("cookieInput").value = "";
    document.getElementById("usernameInput").value = "";
    document.getElementById("passwordInput").value = "";
}

// Event listener for the "Add" button
document.getElementById("addButton").addEventListener("click", () => {
    const cookie = document.getElementById("cookieInput").value;
    const username = document.getElementById("usernameInput").value;
    const password = document.getElementById("passwordInput").value;

    if (cookie && username && password) {
        addRowToTable(cookie, username, password);
        resetInputFields();
        document.getElementById("submitDataButton").style.display = "block";
    } else {
        alert("Please fill in all fields.");
    }
});

// Event delegation for the "Remove" button
document.getElementById("data-table-body").addEventListener("click", (event) => {

    if (event.target.classList.contains("remove-button")) {
        const row = event.target.closest("tr");
        row.remove();
    }
});

// Event listener for the "Submit Data" button
document.getElementById("submitDataButton").addEventListener("click", () => {
    // Display the confirmation modal
    $('#confirmationModal').modal('show');
});


function saveData() {
    // Close the modal
    $('#confirmationModal').modal('hide');

    const tableRows = document.querySelectorAll("#data-table-body tr");
    const rowData = [];

    tableRows.forEach((row) => {
        const cookie = row.dataset.fullCookie;
        const username = row.cells[1].textContent;
        const password = row.dataset.passwordValue; // Retrieve the actual password value

        rowData.push({ cookie, username, password });
    });

    // Output the collected data to the console (you can modify this to save or process the data)
    console.log(rowData);
    processText()
    console.log('====================', listComments)

    $.ajax({
        type: "POST",
        url: "data/insert", // Replace with the actual URL of your Django view
        headers: {
            "X-CSRFToken": csrfToken
        },
        data: {
            data: JSON.stringify(rowData), // Send the entire rowData array as JSON
            comments: JSON.stringify(listComments)
        },
        success: function (response) {
            // Clear the table and hide the Submit button
            tableRows.innerHTML = "";
            document.getElementById("submitDataButton").style.display = "none";

            // Clear the rowData array
            rowData.length = 0;
            window.location.href = "rating/list";
        },
        error: function (xhr, errmsg, err) {
            // Handle any errors that occur during the AJAX request
            alert("Error: " + xhr.status + ": " + xhr.responseText);
        }
    });
}

// Add a paste event listener to the input fields within the "dataTable" table
var dataTable = document.getElementById('dataTable');
var inputFields = dataTable.querySelectorAll('input');

var isPasting = false; // Track if we are currently pasting

inputFields.forEach(function (input) {
    input.addEventListener('paste', function (e) {
        if (isPasting) return; // Prevent simultaneous pasting

        isPasting = true;

        var pastedData = e.clipboardData.getData('text');
        var rows = pastedData.split('\n');

        // Handle the pasted data for the specific input field as needed
        // In this example, we split the data and set it to the corresponding input fields
        var rowCount = 0; // Track the number of rows added
        for (var i = 0; i < rows.length && rowCount < (rows.length - 1); i++) {
            var rowData = rows[i].split('\t'); // Assuming tab-separated data

            if (rowData.length === 3) {
                if (rowCount === 0) {
                    // Paste data into the existing first row
                    for (var j = 0; j < 3; j++) {
                        inputFields[j].value = rowData[j] || ''; // Set value or an empty string
                    }
                } else {
                    // Create a new row in the table (skip the first row)
                    var newRow = dataTable.insertRow(dataTable.rows.length);

                    for (var j = 0; j < 3; j++) {
                        var newCell = newRow.insertCell(j);
                        var newInput = document.createElement('input');
                        newInput.setAttribute('type', (j === 1) ? 'password' : 'text');
                        newInput.setAttribute('class', 'form-control');
                        newInput.placeholder = (j === 0) ? "Tên đăng nhập" : (j === 1) ? "Mật khẩu" : "Cookies";
                        newInput.value = rowData[j] || ''; // Set value or an empty string
                        newCell.appendChild(newInput);
                    }
                }
                rowCount++;
            } else {
                alert('Hãy nhập đủ số lượng cột theo yêu cầu');
                break;
            }
        }

        isPasting = false; // Reset the flag
        e.preventDefault();
    });
});
// Function to gather input data as a list of dictionaries
function getInputData() {
    var data = [];
    var table = document.getElementById("dataTable");
    var rows = table.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) { // Start from index 1 to skip the reference row
        var row = rows[i];
        var cells = row.getElementsByTagName("td");

        var rowData = {
            "username": cells[0].querySelector("input").value,
            "password": cells[1].querySelector("input").value,
            "cookie": cells[2].querySelector("input").value
        };

        data.push(rowData);
    }

    return data;
}

// Event listener for the Submit button within the modal
document.getElementById("submitBtn").addEventListener("click", function () {
    // Get the input data as a list of dictionaries
    var inputData = getInputData();

    // Log the input data as a list of dictionaries to the console
    console.log("Input Data:", inputData);
    inputData.forEach(function (data, index) {
        addRowToTable(data['cookie'], data['username'], data['password']);
        document.getElementById("submitDataButton").style.display = "block";
    });

    // Remove all rows except the reference row
    var table = document.getElementById("dataTable");
    var rows = table.getElementsByTagName("tr");

    // Start from the last row and remove all rows except the reference row (first row)
    for (var i = rows.length - 1; i > 0; i--) {
        table.deleteRow(i);
    }

    // Clear the input fields in the reference row
    var referenceRow = rows[0];
    var cells = referenceRow.getElementsByTagName("td");
    for (var j = 0; j < 3; j++) {
        cells[j].querySelector("input").value = "";
    }
});

// Function to process the entered text
function processText() {
    const textInput = document.getElementById("commentInput");
    const text = textInput.value;

    // Split the text into lines
    const lines = text.split('\n');

    // Log each line to the console and add to a list
    const resultList = [];
    lines.forEach((line, index) => {
        console.log(`Line ${index + 1}: ${line}`);
        listComments.push(line);
    });
}