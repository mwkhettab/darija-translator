<script lang="ts">
	import * as messages from '$lib/paraglide/messages';
</script>

<footer class="footer">
	<p>{messages.footer({ year: new Date().getFullYear() })}</p>
</footer>

<style>
	.footer {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 12px;
		text-align: center;
	}
</style>
