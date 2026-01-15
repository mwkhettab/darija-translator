import type { TranslateResponse } from './types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

const API_BASE_URL = import.meta.env.PROD ? PUBLIC_API_BASE_URL : 'http://localhost:8000/api';

export async function translateText(
	text: string,
	sourceLang: string,
	targetLang: string
): Promise<string> {
	const res = await fetch(`${API_BASE_URL}/translate`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			text,
			source_language: sourceLang,
			target_language: targetLang
		})
	});

	if (!res.ok) {
		throw new Error(await res.text());
	}

	const data: TranslateResponse = await res.json();

	if ('variants' in data) {
		return data.variants.map((v) => v.text).join('\n');
	}

	return data.text;
}

export async function getSupportedLanguages() {
	const res = await fetch(`${API_BASE_URL}/languages`);
	if (!res.ok) {
		throw new Error('Failed to fetch languages');
	}
	return res.json();
}
