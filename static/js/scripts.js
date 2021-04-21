/*!
    * Start Bootstrap - SB Admin v6.0.2 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
(function ($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

})(jQuery);


$(document).ready(function () {
    $('#dataTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
});


window.onload = function () {
    let i;
    // get tab container
    var container = document.getElementById("tabContainer");
    var tabcon = document.getElementById("tabscontent");
    //alert(tabcon.childNodes.item(1));
    // set current tab
    var navitem = document.getElementById("tabHeader_1");

    //store which tab we are on
    if (navitem) {
        var ident = navitem.id.split("_")[1];
        //alert(ident);
        navitem.parentNode.setAttribute("data-current", ident);
        //set current tab with class of activetabheader
        navitem.setAttribute("class", "tabActiveHeader");
    }
    if (tabcon) {
        // hide two tab contents we don't need
        const pages = tabcon.getElementsByTagName("nav");
        for (i = 1; i < pages.length; i++) {
            pages.item(i).style.display = "none";
        }
    }

    if (container) {
        //this adds click event to tabs
        var tabs = container.getElementsByTagName("li");
        for (i = 0; i < tabs.length; i++) {
            tabs[i].onclick = displayPage;
        }
    }
}

// on click of one of tabs
function displayPage() {
    var current = this.parentNode.getAttribute("data-current");
    //remove class of activetabheader and hide old contents
    document.getElementById("tabHeader_" + current).removeAttribute("class");
    document.getElementById("tabpage_" + current).style.display = "none";

    var ident = this.id.split("_")[1];
    //add class of activetabheader to new active tab and show contents
    this.setAttribute("class", "tabActiveHeader");
    document.getElementById("tabpage_" + ident).style.display = "block";
    this.parentNode.setAttribute("data-current", ident);
}
