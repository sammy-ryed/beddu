// Chat functionality for TalkMate AI
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    // Focus on input field
    userInput.focus();
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (!message) {
            return;
        }
        
        // Display user message
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Disable input while waiting for response
        userInput.disabled = true;
        sendButton.disabled = true;
        
        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.innerHTML = '<strong>beedu:</strong> <em>typing...</em>';
        typingDiv.id = 'typing-indicator';
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        
        // Send to backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            // Display bot response
            if (data.success) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
            
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        })
        .catch(error => {
            // Remove typing indicator
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            console.error('Error:', error);
            addMessage('Sorry, I couldn\'t connect. Please check your connection and try again.', 'bot');
            
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        });
    }
    
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'user') {
            messageDiv.innerHTML = `<strong>You:</strong> ${escapeHtml(text)}`;
        } else {
            // Process coping tips to make them collapsible
            const processedText = processCopingTips(text);
            messageDiv.innerHTML = `<strong>beedu:</strong> ${processedText}`;
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Add click handlers for collapsible tips
        if (sender === 'bot') {
            messageDiv.querySelectorAll('.coping-tip-button').forEach(button => {
                button.addEventListener('click', function() {
                    const content = this.nextElementSibling;
                    if (content.style.display === 'none' || !content.style.display) {
                        content.style.display = 'block';
                        this.classList.add('expanded');
                        this.innerHTML = '💡 Hide tip';
                    } else {
                        content.style.display = 'none';
                        this.classList.remove('expanded');
                        this.innerHTML = '💡 Want a tip to help with stress? (click to reveal)';
                    }
                    scrollToBottom();
                });
            });
        }
        
        scrollToBottom();
    }
    
    function processCopingTips(text) {
        // Convert [COPING_TIP_START:X]...[COPING_TIP_END:X] into collapsible elements
        let processed = escapeHtml(text);
        
        // Match coping tip patterns
        const tipPattern = /\[COPING_TIP_START:(\d+)\]([\s\S]*?)\[COPING_TIP_CONTENT:\d+\]([\s\S]*?)\[COPING_TIP_END:\d+\]/g;
        
        processed = processed.replace(tipPattern, (match, id, buttonText, content) => {
            // Clean up the text
            buttonText = buttonText.trim();
            content = content.trim();
            
            return `<div class="coping-tip-container">
                <button class="coping-tip-button">${buttonText}</button>
                <div class="coping-tip-content" style="display: none;">${content}</div>
            </div>`;
        });
        
        return processed;
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
