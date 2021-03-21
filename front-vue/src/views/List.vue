<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <h1>{{todoListName}}</h1>
        <hr>
        <alert :message=message :variant=variant v-if="showMessage"></alert>
        <button id="bouton-add" type="button" class="btn btn-success btn-sm" v-b-modal.todo-add-modal>Add Todo</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" class="text-center">Name</th>
              <th scope="col" class="text-center">Description</th>
              <th scope="col" class="text-center">Last modification</th>
              <th scope="col" class="text-center">Actions</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(todo, index) in todos" :key="index">
              <td class="text-center">{{ todo.name }}</td>
              <td class="text-center">{{todo.description}}</td>
              <td class="text-center">{{todo.lastModif}}
              <td class="text-center">
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.todo-update-modal @click="editTodo(todo.name)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteTodo(todo.name)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTodoModal" id="todo-add-modal" title="Add new todo to list" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group" label="Name:" label-for="form-title-input">
        <b-form-input id="form-title-input" type="text" v-model="addTodoName" required placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-title-group" label="Description:" label-for="form-title-input">
        <b-form-input id="form-title-input" type="text" v-model="addTodoDesc" required placeholder="Enter description">
        </b-form-input>
      </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>


    <b-modal ref="editTodoModal" id="todo-update-modal" title="Update" hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group" label="New name:" label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input" type="text" v-model="editTodoNewName" required placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group" label="New description:" label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input" type="text" v-model="editTodoNewDesc" required placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>
<style scoped>
h1{
  padding-left:10px;
  padding-top:20px
}

#bouton-add{
  margin-left: 5%;
}
</style>

<script>
import Alert from '../components/Alert.vue';
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      addTodoName:'',
      addTodoDesc:'',
      editTodoNewName:'',
      editTodoOldName:'',
      editTodoNewDesc:'',
      deletetodoName:'',
      todoListName:this.$route.params.todo_list_name,
      message:'',
      showMessage:false,
      variant:''
    };
  },
  methods: {
    getTodos() {
      const path = `http://localhost:5001/api/lists/todos/${this.todoListName}`;
      axios.get(path)
        .then((res) => {
          this.todos = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  
    addTodo(payload) {
      const path = `http://localhost:5001/api/lists/todos/${this.todoListName}`;
      axios.put(path, payload)
        .then((res) => {
          console.log(res.data)
          this.message=res.data.message
          this.variant="success"
          this.showMessage=true
          this.getTodos()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.message=error.response.data.message
          this.variant="danger"
          this.showMessage=true
          this.getTodos()
        });
    },
    initForm() {
      this.addTodoName=''
      this.addTodoDesc=''
      this.editTodoNewName=''
      this.editTodoOldName=''
      this.editTodoNewDesc=''
      this.deletetodoName=''
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      const payload = {
        nom: this.addTodoName,
        description: this.addTodoDesc
      };
      this.addTodo(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      this.initForm();
    },
    editTodo(todo) {
      this.editTodoOldName = todo;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      const payload = {
        newName: this.editTodoNewName,
        newDesc: this.editTodoNewDesc
      };
      this.updateTodo(payload, this.editTodoOldName);
    },
    updateTodo(payload, todoOldName) {
      const path = `http://localhost:5001/api/lists/todos/${this.todoListName}/${todoOldName}`;
      axios.patch(path, payload)
        .then((res) => {
          this.getTodos();
          this.message=res.data.message
          this.variant="success"
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.message=error.response.data.message 
          this.variant="danger"      
          this.showMessage = true;
          this.getTodos();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      this.initForm();
      this.getTodos(); // why?
    },
    removeTodo(todoName) {
      const path = `http://localhost:5001/api/lists/todos/${this.todoListName}/${todoName}`;
      axios.delete(path)
        .then((res) => {
          this.message=res.data.message
          this.variant="success"
          this.showMessage = true;
          this.getTodos();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.message=error.response.data.message   
          this.variant="danger"       
          this.showMessage = true;
          this.getTodos();
        });
    },
    onDeleteTodo(todoName) {
      this.removeTodo(todoName);
    },


  },
  
    created() {
      this.getTodos();
    },
  components: {
    alert: Alert,
  },
  
};
</script>