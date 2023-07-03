import { BASE_API_URI } from '$lib/constants';
import { session } from '$lib/store/user.store';
import type { PageLoad } from '.svelte-kit/types/src/routes/chat/$types';
import { redirect } from '@sveltejs/kit';
import { get } from 'svelte/store';

export const load: PageLoad = async ({ fetch }) => {
	const $session = get(session);
	if (!$session.isAuthenticated) {
		throw redirect(307, '/');
	} else {
		const res = await fetch(`${BASE_API_URI}/list-contacts/?username=${$session.user.username}`, {
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		});
		// let data;
		// res.then(function(result) {
		// 	// here you can use the result of promiseB
		// 	data = result.json();
		// });
		let data = await res.json()
		console.log(data);
		// console.log("updar dekh")
		// console.log(res.json().data)
		return {
			userContacts: res.ok && data['accepted']
		};
	}
};
