document.addEventListener('DOMContentLoaded', function(){

	try{
	edits = document.querySelectorAll('.edit');
	edits.forEach(edit => {
		edit.addEventListener('submit', ()=>{
			alert('You just edited this item');
		})
	})}
	catch{}

	try{
	add = document.querySelector('#add');
	add.onclick = function(){
		document.querySelector('#main').style.display = 'none';
		document.querySelector('#add_div').style.display = 'block';
	}}
	catch{}

	try{
	dels = document.querySelectorAll('#delete')
	dels.forEach(del =>{
		del.onsubmit = function(){
			return confirm('Do you really want to delete this item?');
		}
	})}
	catch{}

	try{
	checkout = document.querySelector('#checkout');
	checkout.onsubmit = ()=>{
		return confirm('Do you want to checkout?');
	}}
	catch{}

})