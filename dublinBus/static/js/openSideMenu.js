function openSideMenu() {
    if (window.screen.width >= 992) {
        // open the menu 
        console.log('open side menu')
        document.getElementById('open-menu-btn').click();
    } 
}
function selectInfo() {
    document.querySelector('#info-tab').click();
}
openSideMenu();
selectInfo();