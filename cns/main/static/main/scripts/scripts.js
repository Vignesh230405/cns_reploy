function setupGlobalChatHeaderLink() {
    const globalChatHeader = document.querySelector('.chat-option.active');
    if (globalChatHeader) {
        globalChatHeader.addEventListener('click', () => {
            window.location.href = globalChatUrl;
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupGlobalChatHeaderLink();
});
