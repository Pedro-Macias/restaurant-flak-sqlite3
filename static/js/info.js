// seleccionamos todos los botones de borrar y le ponemos una alerta
const btnBorrar = document.querySelectorAll('.boton_borrar')
if (btnBorrar){
    const btnArreglo = Array.from(btnBorrar);
    btnArreglo.forEach((btn) =>{
        btn.addEventListener('click',(e) => {
            if (!confirm('Estas seguro de Eliminarlo?')){
                e.preventDefault();
            }
        });
    });

}