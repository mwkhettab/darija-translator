<script lang="ts">
	import { onMount } from 'svelte';
	import { getLocale } from '$lib/paraglide/runtime';
	import * as m from '$lib/paraglide/messages';

	import { translateText, getSupportedLanguages } from './api';
	import type { Direction, Language, HistoryItem } from './types';

	const locale = getLocale();

	/* ------------------ COPY ------------------ */
	const copy = {
		title: m['translate.title'](),
		inputPlaceholder: m['translate.input.placeholder'](),
		switch: m['translate.switch'](),
		translate: m['translate.translate'](),
		translating: m['translate.translating'](),
		clear: m['translate.clear'](),
		resultTitle: m['translate.result.title'](),
		historyTitle: m['translate.history.title'](),
		historyClear: m['translate.history.clear'](),
		copy: m['translate.copy'](),
		copied: m['translate.copied'](),
		errorLoadLanguages: m['error.loadLanguages'](),
		errorTranslationFailed: m['error.translationFailed'](),
		darija: m['darija']()
	};

	/* ------------------ STATE ------------------ */
	let languages: Language[] = [];
	let direction: Direction = 'darija-to-lang';
	let selectedLanguage: Language | null = null;

	let inputText = '';
	let outputText = '';
	let isTranslating = false;
	let errorMessage = '';
	let copySuccess = false;

	let history: HistoryItem[] = [];

	/* ------------------ HELPERS ------------------ */
	const labelForLocale = (names: { en: string; fr: string; ar: string }): string =>
		locale === 'fr' ? names.fr : locale === 'ar' ? names.ar : names.en;

	const getSourceTarget = () => {
		if (!selectedLanguage) return null;

		return direction === 'darija-to-lang'
			? { source: 'ary', target: selectedLanguage.code }
			: { source: selectedLanguage.code, target: 'ary' };
	};

	/* ------------------ INIT ------------------ */
	onMount(async () => {
		try {
			const saved = localStorage.getItem('translationHistory');
			if (saved) history = JSON.parse(saved);
		} catch {
			history = [];
		}

		try {
			const data = (await getSupportedLanguages()) as Record<
				string,
				{ en: string; fr: string; ar: string }
			>;

			languages = Object.entries(data)
				.filter(([code]) => code !== 'ary')
				.map(([code, names]) => ({
					code,
					label: labelForLocale(names)
				}));

			selectedLanguage = languages.find((l) => l.code === 'en') ?? languages[0];
		} catch {
			errorMessage = copy.errorLoadLanguages;
		}
	});

	/* ------------------ ACTIONS ------------------ */
	function switchDirection() {
		direction = direction === 'darija-to-lang' ? 'lang-to-darija' : 'darija-to-lang';

		inputText = '';
		outputText = '';
		errorMessage = '';
	}

	async function doTranslate() {
		if (!inputText.trim() || !selectedLanguage) return;

		const pair = getSourceTarget();
		if (!pair) return;

		isTranslating = true;
		errorMessage = '';
		outputText = '';

		try {
			outputText = await translateText(inputText, pair.source, pair.target);

			history = [{ input: inputText, output: outputText }, ...history].slice(0, 10);
			localStorage.setItem('translationHistory', JSON.stringify(history));
		} catch {
			errorMessage = copy.errorTranslationFailed;
		} finally {
			isTranslating = false;
		}
	}

	async function copyToClipboard() {
		if (!outputText) return;

		await navigator.clipboard.writeText(outputText);
		copySuccess = true;

		setTimeout(() => {
			copySuccess = false;
		}, 2000);
	}

	function clearAll() {
		inputText = '';
		outputText = '';
		errorMessage = '';
	}

	function clearHistory() {
		history = [];
		localStorage.removeItem('translationHistory');
	}
</script>

<section class="translate">
	<div class="translate-content">
		<h2 class="translate-title">{copy.title}</h2>

		{#if errorMessage && !inputText}
			<div class="error-message">{errorMessage}</div>
		{/if}

		{#if selectedLanguage}
			<div class="direction-row">
				{#if direction === 'darija-to-lang'}
					<span class="direction-label">{copy.darija}</span>
				{:else}
					<select bind:value={selectedLanguage} class="language-select">
						{#each languages as lang (lang.code)}
							<option value={lang}>{lang.label}</option>
						{/each}
					</select>
				{/if}

				<span class="arrow">→</span>

				{#if direction === 'darija-to-lang'}
					<select bind:value={selectedLanguage} class="language-select">
						{#each languages as lang (lang.code)}
							<option value={lang}>{lang.label}</option>
						{/each}
					</select>
				{:else}
					<span class="direction-label">{copy.darija}</span>
				{/if}

				<button class="switch-btn" on:click={switchDirection}>
					{copy.switch}
				</button>
			</div>
		{/if}

		<div class="translate-card">
			<textarea
				class="translate-input"
				bind:value={inputText}
				placeholder={copy.inputPlaceholder}
				rows="4"
			></textarea>

			<div class="translate-actions">
				<button
					class="translate-btn primary"
					on:click={doTranslate}
					disabled={isTranslating || !inputText.trim() || !selectedLanguage}
				>
					{isTranslating ? copy.translating : copy.translate}
				</button>
			</div>
		</div>

		<div class="translate-card output">
			<h3>{copy.resultTitle}</h3>

			{#if errorMessage && inputText}
				<p class="error-text">{errorMessage}</p>
			{:else if isTranslating}
				<div class="loading">
					<div class="spinner"></div>
					<p>{copy.translating}</p>
				</div>
			{:else}
				<p class="translate-result">{outputText || '—'}</p>
			{/if}

			<div class="translate-actions">
				{#if outputText}
					<button class="translate-btn copy" on:click={copyToClipboard}>
						{copySuccess ? copy.copied : copy.copy}
					</button>
				{/if}

				<button class="translate-btn" on:click={clearAll}>
					{copy.clear}
				</button>
			</div>
		</div>

		{#if history.length > 0}
			<div class="history">
				<div class="history-header">
					<h3>{copy.historyTitle}</h3>
					<button class="clear-history-btn" on:click={clearHistory}>
						{copy.historyClear}
					</button>
				</div>

				{#each history as item (item.input + item.output)}
					<div class="history-item">
						<p class="history-input">{item.input}</p>
						<p class="history-output">{item.output}</p>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</section>

<style>
	.translate {
		background: var(--moroccan-red);
		width: 100%;
		display: flex;
		justify-content: center;
		padding: 4rem 1.25rem;
		box-sizing: border-box;
	}

	.translate-content {
		width: 100%;
		max-width: 720px;
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.translate-title {
		text-align: center;
		font-size: 2rem;
		color: white;
		margin: 0;
	}

	.error-message {
		background: rgba(255, 255, 255, 0.2);
		color: white;
		padding: 1rem;
		border-radius: 8px;
		text-align: center;
		font-weight: 600;
	}

	.error-text {
		color: #d32f2f;
		font-weight: 600;
	}

	.direction-row {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 0.75rem;
		flex-wrap: wrap;
		color: white;
		font-weight: 600;
	}

	.direction-label {
		background: var(--moroccan-green);
		padding: 0.45rem 1rem;
		border-radius: 999px;
	}

	.language-select {
		appearance: none;
		background: white;
		border-radius: 999px;
		padding: 0.45rem 2.25rem 0.45rem 1rem;
		border: none;
		font-weight: 600;
		color: var(--moroccan-red);
		cursor: pointer;
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M6 9l6 6 6-6' stroke='%23900' stroke-width='2'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.75rem center;
		background-size: 1rem;
	}

	.switch-btn {
		background: transparent;
		border: 2px solid white;
		color: white;
		padding: 0.4rem 1.25rem;
		border-radius: 999px;
		cursor: pointer;
		font-weight: 600;
		transition: all 0.2s;
	}

	.switch-btn:hover {
		background: white;
		color: var(--moroccan-red);
	}

	.translate-card {
		background: white;
		border-radius: 16px;
		padding: 1.75rem;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
		border-top: 6px solid var(--moroccan-red);
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
	}

	.translate-card.output {
		border-top-color: var(--moroccan-green);
	}

	.translate-input {
		width: 100%;
		padding: 1rem;
		border-radius: 10px;
		border: 2px solid #ddd;
		font-size: 1rem;
		font-family: inherit;
		box-sizing: border-box;
		resize: vertical;
	}

	.translate-result {
		color: var(--moroccan-green);
		font-weight: 600;
		font-size: 1.1rem;
		min-height: 2rem;
		white-space: pre-wrap;
	}

	.loading {
		display: flex;
		align-items: center;
		gap: 1rem;
		color: #666;
	}

	.spinner {
		width: 24px;
		height: 24px;
		border: 3px solid #ddd;
		border-top-color: var(--moroccan-red);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.translate-actions {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}

	.translate-btn {
		padding: 0.7rem 1.75rem;
		border-radius: 8px;
		font-weight: 600;
		border: none;
		cursor: pointer;
		transition: opacity 0.2s;
	}

	.translate-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.translate-btn.primary {
		background: var(--moroccan-red);
		color: white;
	}

	.translate-btn.copy {
		background: var(--moroccan-green);
		color: white;
	}

	.history {
		background: rgba(255, 255, 255, 0.15);
		border-radius: 16px;
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.history-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
	}

	.history h3 {
		color: white;
		font-size: 0.85rem;
		text-transform: uppercase;
		margin: 0;
	}

	.clear-history-btn {
		background: rgba(255, 255, 255, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 0.4rem 1rem;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.85rem;
		font-weight: 600;
		transition: all 0.2s;
	}

	.clear-history-btn:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	.history-item {
		background: white;
		border-radius: 12px;
		padding: 1rem;
		border-left: 6px solid var(--moroccan-green);
	}

	.history-input {
		font-weight: 600;
		margin: 0 0 0.25rem;
	}

	.history-output {
		margin: 0;
		color: var(--moroccan-green);
		font-weight: 600;
		white-space: pre-wrap;
	}
</style>
