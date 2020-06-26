function getPrice(item) {
    if (item.normal_discount && item.cartbox_discount) {
        return `
            <p><strong>Original Price:</strong> ${item.old_price}₺</p>
            <p><strong>Default Price:</strong> ${item.default_price}₺</p>
            <p><strong>Normal Discount:</strong> ${Math.round(item.normal_discount * 100)}%</p>
            <p><strong>Cartbox Price:</strong> ${item.cartbox_price}₺</p>
            <p><strong>Cartbox Discount:</strong> ${Math.round(item.cartbox_discount * 100)}%</p>
        `;
    }
    else if (item.normal_discount) {
        return `
            <p><strong>Original Price:</strong> ${item.old_price}₺</p>
            <p><strong>Default Price:</strong> ${item.default_price}₺</p>
            <p><strong>Normal Discount:</strong> ${Math.round(item.normal_discount * 100)}%</p>
        `;
    }
    else if (item.cartbox_discount) {
        return `
            <p><strong>Original Price:</strong> ${item.default_price}₺</p>
            <p><strong>Cartbox Price:</strong> ${item.cartbox_price}₺</p>
            <p><strong>Cartbox Discount:</strong> ${Math.round(item.cartbox_discount * 100)}%</p>
        `;
    }
    else {
        return `
            <p><strong>Default Price:</strong> ${item.default_price}₺</p>
            <p><strong>Discount:</strong> None </p>
        `;
    }
}

function itemTemplate(item) {
    return `
    <li>
        <img src="${item.image_url}" />
        <h4>${item.details.brand}</h4>
        <h5>${item.details.description}</h5> 
        ${getPrice(item)}
        <p><strong>Threshold:</strong> ${item.threshold}₺</p>
        <a href=${item.url} target="_blank" style="color: #58d5f7">Visit Item Website</a> 
    </li>
    `;
}

function getSelectedItemURL() {
    var selected_item = document.getElementsByClassName("selected")[0];
    var selected_item_url = selected_item.children[selected_item.children.length - 1].href;
    return selected_item_url;
}

async function listItems() {
    // get items
    let tracked_items = await eel.getItemsJSON()();
    let info = await tracked_items.map(itemTemplate).join("");
    document.getElementById("app").innerHTML = `${info} `;

    // item selector
    var items = document.querySelectorAll("#list li");
    for (var i = 0; i < items.length; i++) {
        items[i].onclick = function () {
            for (var j = 0; j < items.length; j++) {
                items[j].classList.remove('selected');
            }
            this.classList.add('selected');
        };
    }

    window.addEventListener("mouseup", async function (event) {
        var list = document.getElementById("list");
        var item_list = document.getElementById("item-div");
        var conds = document.getElementsByClassName("cond-vis");

        if (event.target == list || event.target == conds[0] || event.target == conds[1] ||
            event.composedPath().toString().indexOf("[object HTMLLIElement]") >= 0) {
            for (var i = 0; i < conds.length; i++) {
                conds[i].style.visibility = "visible";
            }

            item_list.classList.remove("item-list-hidden");
            item_list.classList.add("item-list");
        } else {
            for (var i = 0; i < items.length; i++) {
                items[i].classList.remove('selected');
            }

            for (var i = 0; i < conds.length; i++) {
                conds[i].style.visibility = "hidden";
            }

            await sleep(400);
            item_list.classList.remove("item-list");
            item_list.classList.add("item-list-hidden");
        }
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms || DEF_DELAY));
}

async function addItem() {
    var url = document.getElementById('url-box').value;
    var threshold = document.getElementById('threshold-box').value;
    var sync_button = document.getElementById('sync-button');

    if (url === "") {
        Swal.fire({
            title: 'Enter URL',
            icon: 'warning'
        });
    }
    else if (threshold === "" || isNaN(threshold) || threshold < 0) {
        Swal.fire({
            title: 'Invalid Threshold!',
            text: 'Enter a valid threshold.',
            icon: 'error'
        });
    }
    else {
        let add_result = await eel.addItem(url, threshold)();
        if (add_result) {
            Swal.fire({
                title: 'Added Item',
                icon: 'success'
            });
            document.getElementById('url-box').value = "";
            document.getElementById('threshold-box').value = "";
            sync_button.classList.remove("cond-vis-sync");
            listItems();
        }
        else {
            Swal.fire({
                title: 'Item Not Found!',
                text: 'Enter a valid URL',
                icon: 'error'
            });
        }
    }
}

async function removeItem() {
    var sync_button = document.getElementById('sync-button');
    var selected_item_url = getSelectedItemURL();
    Swal.fire({
        title: 'Are you sure?',
        text: 'You will not be able to recover this item!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, keep it'
    }).then(async (result) => {
        if (result.value) {
            var remove_result = await eel.removeItem(selected_item_url)();
            if (remove_result) {
                Swal.fire(
                    'Deleted!',
                    'Your item has been deleted.',
                    'success'
                )
                sync_button.classList.remove("cond-vis-sync");
                listItems();
            }
            else {
                Swal.fire(
                    'Oops!',
                    'Your item cannot be deleted.',
                    'error'
                )
            }

        } else if (result.dismiss === Swal.DismissReason.cancel) {
            Swal.fire(
                'Cancelled',
                'Your item is safe :)',
                'error'
            )
        }
    });
}

async function editThreshold() {
    var sync_button = document.getElementById('sync-button');
    var selected_item_url = getSelectedItemURL();
    const { value: threshold } = await Swal.fire({
        title: 'Enter new price threshold',
        input: 'text',
        inputPlaceholder: 'Threshold',
        showCancelButton: true,
        inputValidator: (value) => {
            if (value === "" || isNaN(value) || value < 0) {
                return 'You need to write something!'
            }
        }
    })

    if (threshold) {
        var edit_result = await eel.editThreshold(selected_item_url, threshold)();
        if (edit_result) {
            Swal.fire(
                'Editted Threshold!',
                `Your item has a new price threshold: ${threshold}₺`,
                'success'
            )
            sync_button.classList.remove("cond-vis-sync");
            listItems();
        }
        else {
            Swal.fire(
                'Oops!',
                'Your price threshold cannot be editted.',
                'error'
            )
        }
    }
}

async function syncItems() {
    var sync_button = document.getElementById('sync-button');
    sync_button.innerHTML = `<i class="material-icons"
                            style="font-size:20px; position: relative; top: 4px;">sync</i> Syncing...`;

    await eel.uploadItems()();

    sync_button.classList.add("cond-vis-sync");
    await sleep(400);
    sync_button.innerHTML = `<i class="material-icons"
                            style="font-size:20px; position: relative; top: 4px;">sync</i> Sync Now`;

    Swal.fire({
        title: 'Synced',
        icon: 'success'
    });
}

listItems();


