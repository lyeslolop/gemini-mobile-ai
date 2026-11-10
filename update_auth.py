import re
import os

target_files = [
    r'C:\Users\pc\Desktop\gemini-mobile-ai\index.html',
    r'C:\Users\pc\Desktop\Gemini-Interface.html'
]

new_firebase_script = """    <!-- Firebase JS SDK (v10 Modular) -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
        import { 
            getAuth, 
            signInWithEmailAndPassword, 
            createUserWithEmailAndPassword, 
            onAuthStateChanged, 
            signOut 
        } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";

        const firebaseConfig = {
            apiKey: "AIzaSyDEXl7V0dFPhhUMsHvas_0ANPOggsacFpk",
            authDomain: "ia-dope.firebaseapp.com",
            projectId: "ia-dope",
            storageBucket: "ia-dope.firebasestorage.app",
            messagingSenderId: "642450934502",
            appId: "1:642450934502:web:23aa0dfd6749ee1ac44927",
            measurementId: "G-E0151HX86X"
        };

        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);

        window.firebaseApp = app;
        window.firebaseAuth = auth;

        window.loginWithEmailPassword = async function(e) {
            if (e) e.preventDefault();
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            const errorBox = document.getElementById('authErrorBox');
            const submitBtn = document.getElementById('authSubmitBtn');

            if (!email || !password) {
                if (errorBox) {
                    errorBox.textContent = "Veuillez renseigner votre email et mot de passe.";
                    errorBox.classList.remove('hidden');
                }
                return;
            }

            if (submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Connexion...';
            if (errorBox) errorBox.classList.add('hidden');

            try {
                const userCredential = await signInWithEmailAndPassword(auth, email, password);
                if (window.handleUserLogin) window.handleUserLogin(userCredential.user);
            } catch (error) {
                console.error("Firebase Login Error:", error);
                if (errorBox) {
                    let msg = "Erreur de connexion.";
                    if (error.code === 'auth/invalid-credential' || error.code === 'auth/wrong-password') {
                        msg = "Email ou mot de passe incorrect.";
                    } else if (error.code === 'auth/user-not-found') {
                        msg = "Aucun compte associé à cet email.";
                    } else if (error.code === 'auth/invalid-email') {
                        msg = "Format d'email invalide.";
                    } else {
                        msg = error.message;
                    }
                    errorBox.textContent = msg;
                    errorBox.classList.remove('hidden');
                }
                if (submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-right-to-bracket mr-2"></i> Se connecter';
            }
        };

        window.registerWithEmailPassword = async function() {
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            const errorBox = document.getElementById('authErrorBox');

            if (!email || !password) {
                if (errorBox) {
                    errorBox.textContent = "Indiquez l'email et le mot de passe à créer.";
                    errorBox.classList.remove('hidden');
                }
                return;
            }

            try {
                const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                if (window.handleUserLogin) window.handleUserLogin(userCredential.user);
            } catch (error) {
                if (errorBox) {
                    errorBox.textContent = "Erreur création de compte : " + error.message;
                    errorBox.classList.remove('hidden');
                }
            }
        };

        window.bypassAuth = function() {
            localStorage.setItem('gemini_local_bypass', 'true');
            const authModal = document.getElementById('authModal');
            if (authModal) authModal.classList.add('hidden');
            if (window.showToast) window.showToast('Mode test local activé !');
        };

        window.showAuthModal = function() {
            const authModal = document.getElementById('authModal');
            if (authModal) authModal.classList.remove('hidden');
        };

        window.handleUserLogin = function(user) {
            const profile = {
                name: user.displayName || user.email.split('@')[0],
                email: user.email,
                photoURL: user.photoURL,
                uid: user.uid
            };
            localStorage.setItem('gemini_user_profile', JSON.stringify(profile));
            if (window.updateUserProfileUI) window.updateUserProfileUI(profile);
            const authModal = document.getElementById('authModal');
            if (authModal) authModal.classList.add('hidden');
            if (window.showToast) window.showToast(`Connecté : ${profile.email}`);
        };

        window.logoutFirebase = async function() {
            try {
                await signOut(auth);
                localStorage.removeItem('gemini_user_profile');
                localStorage.removeItem('gemini_local_bypass');
                location.reload();
            } catch (err) {
                console.error("Logout error:", err);
            }
        };

        onAuthStateChanged(auth, (user) => {
            if (user) {
                if (window.handleUserLogin) window.handleUserLogin(user);
            } else {
                const bypass = localStorage.getItem('gemini_local_bypass');
                if (!bypass && window.showAuthModal) {
                    window.showAuthModal();
                }
            }
        });
    </script>"""

new_auth_modal = """    <!-- ==================== 0. FIREBASE AUTHENTICATION OVERLAY ==================== -->
    <div id="authModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-[100] flex items-center justify-center p-4 transition-all duration-300">
        <div class="bg-white dark:bg-[#1e1f20] w-full max-w-md rounded-3xl border border-gray-200 dark:border-gray-700/80 shadow-2xl p-7 text-center animate-fadeIn">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-500 via-indigo-500 to-purple-500 mx-auto flex items-center justify-center text-white text-2xl shadow-lg mb-4">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h2 class="font-display text-2xl font-bold text-gray-900 dark:text-white mb-1.5">Authentification Firebase</h2>
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-5">
                Connectez-vous avec votre e-mail et mot de passe pour accéder à votre IA.
            </p>

            <div id="authErrorBox" class="hidden mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 text-xs text-left"></div>

            <form onsubmit="loginWithEmailPassword(event)" class="space-y-3.5 text-left">
                <div>
                    <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Adresse e-mail</label>
                    <div class="relative">
                        <i class="fa-solid fa-envelope absolute left-3.5 top-3.5 text-gray-400 text-xs"></i>
                        <input type="email" id="loginEmail" required placeholder="nom@exemple.com" class="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-gray-100 dark:bg-[#131314] border border-gray-300 dark:border-gray-700 focus:outline-none focus:border-blue-500 text-sm">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Mot de passe</label>
                    <div class="relative">
                        <i class="fa-solid fa-key absolute left-3.5 top-3.5 text-gray-400 text-xs"></i>
                        <input type="password" id="loginPassword" required placeholder="••••••••" class="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-gray-100 dark:bg-[#131314] border border-gray-300 dark:border-gray-700 focus:outline-none focus:border-blue-500 text-sm">
                    </div>
                </div>

                <button type="submit" id="authSubmitBtn" class="w-full py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm flex items-center justify-center shadow-md transition-all cursor-pointer mt-2">
                    <i class="fa-solid fa-right-to-bracket mr-2"></i> Se connecter
                </button>
            </form>

            <div class="flex items-center justify-between mt-4 pt-3 border-t border-gray-200 dark:border-gray-700/60 text-xs">
                <button type="button" onclick="registerWithEmailPassword()" class="text-blue-500 hover:underline cursor-pointer">
                    Créer un compte
                </button>
                <button type="button" onclick="bypassAuth()" class="text-gray-400 hover:text-gray-200 cursor-pointer">
                    Mode test local
                </button>
            </div>

            <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-4">
                Projet Firebase : <code class="text-blue-400 font-mono">ia-dope</code>
            </p>
        </div>
    </div>"""

for fpath in target_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Firebase script
    content = re.sub(r'<!-- Firebase JS SDK.*?</script>', new_firebase_script, content, flags=re.DOTALL)

    # Replace Auth modal
    content = re.sub(r'<!-- ==================== 0\. FIREBASE AUTHENTICATION OVERLAY.*?<!-- MOBILE OVERLAY FOR SIDEBAR', 
                     new_auth_modal + '\n\n    <!-- MOBILE OVERLAY FOR SIDEBAR', 
                     content, flags=re.DOTALL)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Updated:', fpath)
