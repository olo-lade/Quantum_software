// shared.js — Quantum API Dashboard
const BASE = 'http://127.0.0.1:8000';
const KEY_STORE = 'qapi_key';

// Persist API key across pages
function loadKey() {
  const saved = localStorage.getItem(KEY_STORE) || '';
  document.querySelectorAll('.key-input').forEach(el => el.value = saved);
}
function saveKey(val) {
  localStorage.setItem(KEY_STORE, val);
}
function getKey() {
  const k = (document.querySelector('.key-input')?.value || '').trim();
  if (!k) { alert('Paste your X-Api-Key in the top bar first.'); return null; }
  saveKey(k);
  return k;
}

// Show result in a result box
function show(id, data, isError = false) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
  el.className = 'result' + (isError ? ' error' : '');
}

// Generic API call
async function call(endpoint, body, resultId, btn, method = 'POST') {
  const key = getKey(); if (!key) return;
  btn.disabled = true;
  show(resultId, 'Running…');
  try {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json', 'X-Api-Key': key },
    };
    if (method !== 'DELETE') opts.body = JSON.stringify(body);
    const res = await fetch(BASE + endpoint, opts);
    const data = await res.json();
    show(resultId, data, !res.ok);
  } catch (e) {
    show(resultId, { error: e.message }, true);
  } finally {
    btn.disabled = false;
  }
}

// Highlight active nav link
function setActiveNav() {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  loadKey();
  setActiveNav();
  document.querySelectorAll('.key-input').forEach(el => {
    el.addEventListener('input', () => saveKey(el.value.trim()));
  });
});
