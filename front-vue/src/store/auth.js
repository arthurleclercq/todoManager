import axios from 'axios';
import {
	AUTH_REQUEST,
	AUTH_ERROR,
	AUTH_SUCCESS,
	AUTH_LOGOUT
} from "@/store/actions";

const state = {
	token: localStorage.getItem('jwt') || '',
	status: '',
	user:localStorage.getItem('user') || '',
};

const getters = {
	isAuthenticated: state => !!state.token,
	authStatus: state => state.status,
	username:state => state.user
};

const actions = {
	[AUTH_REQUEST]: ({commit}, user) => {
		return new Promise((resolve, reject) => {
			commit(AUTH_REQUEST);
			const path = 'http://localhost:5001/api/login';
			axios.post(path, user).then(res => {
				const token = res.data.token;
				const username=user.user
				localStorage.setItem('jwt', token);
				localStorage.setItem("user",user.user);
				commit(AUTH_SUCCESS, {token,username});

				resolve(res.data);
			}).catch(error => {
				console.log(error)
				commit(AUTH_ERROR);
				localStorage.removeItem('jwt');
				reject(error.response.data);
			});
		});
	},
	[AUTH_LOGOUT]: ({commit}) => {
		return new Promise((resolve) => {
			commit(AUTH_LOGOUT);
			localStorage.removeItem('jwt');
			resolve();
		});
	}
};

const mutations = {
	[AUTH_REQUEST]: (state) => {
		state.status = 'loading';
	},
	[AUTH_SUCCESS]: (state, {token,username}) => {
		
		state.status = 'success';
		state.token = token;
		state.user=username
	},
	[AUTH_ERROR]: (state) => {
		state.status = 'error';
	},
	[AUTH_LOGOUT]: (state) => {
		state.status = 'disconnected';
		state.token = "";
	},
};

export default {
	state,
	getters,
	actions,
	mutations
};
