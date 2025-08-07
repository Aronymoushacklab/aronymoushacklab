        // Initialize our reality distortion field
        document.addEventListener('DOMContentLoaded', function() {
            // Glitch text effect for the scrambled text
            const scrambledElements = document.querySelectorAll('.scrambled-text');
            setInterval(() => {
                scrambledElements.forEach(elem => {
                    const originalText = elem.getAttribute('data-original') || elem.innerText;
                    if (!elem.getAttribute('data-original')) {
                        elem.setAttribute('data-original', originalText);
                    }
                    
                    // Random chance to scramble
                    if (Math.random() > 0.7) {
                        let scrambledText = '';
                        for(let i = 0; i < originalText.length; i++) {
                            if (Math.random() > 0.7) {
                                const chars = "!@#$%^&*()_+-=[]{}|;':,./<>?`~";
                                scrambledText += chars.charAt(Math.floor(Math.random() * chars.length));
                            } else {
                                scrambledText += originalText[i];
                            }
                        }
                        elem.innerText = scrambledText;
                    } else {
                        elem.innerText = originalText;
                    }
                });
            }, 100);
            
            // Modal handling
            const orderButtons = document.querySelectorAll('.order-btn');
            const modal = document.getElementById('quoteModal');
            const closeBtn = document.querySelector('.close-btn');
            
            orderButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Get item details
                    const itemElement = this.closest('.item');
                    if (itemElement) {
                        const itemName = itemElement.querySelector('h3').innerText.split(' <')[0];
                        const itemPrice = itemElement.querySelector('.price').innerText.split(' [')[0];
                        
                        document.getElementById('quote-item-name').innerText = itemName;
                        document.getElementById('quote-price').innerText = itemPrice;
                    }
                    
                    modal.style.display = 'flex';
                    
                    // Simulate transmission interference
                    setTimeout(() => {
                        const warningText = document.querySelector('.warning-text');
                        warningText.style.animation = 'glitch 0.3s infinite';
                    }, 2000);
                });
            });
            
            closeBtn.addEventListener('click', function() {
                modal.style.display = 'none';
            });
            
            // Close modal if clicked outside
            window.addEventListener('click', function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            });
            
            // Simulate chat activity
            const chatSystem = document.querySelector('.chat-system');
            const chatUsers = ['PsychonautPrime', 'VeilWalker', 'ArsenalKeeper', 'QuantumResistance', 'PatternSeeker'];
            const chatMessages = [
                'Has anyone tested the new crystals from sector 7?',
                'Be careful with the dosage on the new batch. WAY more potent.',
                'Feds monitoring dropsite alpha. Use caution.',
                'Anyone have schematics for a DIY consciousness firewall?',
                'My perception filters detected anomalies near the old military base.',
                'Trust nothing. Question everything. Especially this message.',
                'New shipment confirmed. Use the old codes.',
                'The veil is thinning. Stock up while you can.'
            ];
            
            setInterval(() => {
                if (Math.random() > 0.7) {
                    const newMessage = document.createElement('div');
                    newMessage.className = 'chat-message';
                    
                    const randomUser = chatUsers[Math.floor(Math.random() * chatUsers.length)];
                    const randomMessage = chatMessages[Math.floor(Math.random() * chatMessages.length)];
                    
                    const time = new Date();
                    const timeStr = `[${time.getHours().toString().padStart(2, '0')}:${time.getMinutes().toString().padStart(2, '0')}]`;
                    
                    newMessage.innerHTML = `
                        <span class="sender">${randomUser}:</span>
                        <span class="timestamp">${timeStr}</span>
                        <div class="text">${randomMessage}</div>
                    `;
                    
                    chatSystem.appendChild(newMessage);
                    chatSystem.scrollTop = chatSystem.scrollHeight;
                    
                    // Limit chat history
                    if (chatSystem.children.length > 20) {
                        chatSystem.removeChild(chatSystem.children[0]);
                    }
                }
            }, 10000);
        });