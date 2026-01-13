export type Direction = 'darija-to-lang' | 'lang-to-darija';

export type Language = {
	code: string;
	label: string;
};

export type TranslationVariant = {
	script: 'latin' | 'arabic';
	text: string;
};

export type TranslateResponse = { text: string } | { variants: TranslationVariant[] };

export type HistoryItem = {
	input: string;
	output: string;
};
