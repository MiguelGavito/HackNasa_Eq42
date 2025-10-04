import React from 'react';
import './meteorSelection.css'; // Asegúrate de crear este archivo para los estilos

export function MeteorSelection() {
    return (
        <>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            <div className="image">
                <form className="meteor-form">
                    <h2>Selecciona tu meteorito</h2>
                    <label>
                        Nombre:
                        <input type="text" name="nombre" />
                    </label>
                    <label>
                        Tipo:
                        <select name="tipo">
                            <option value="hierro">Hierro</option>
                            <option value="piedra">Piedra</option>
                            <option value="mixto">Mixto</option>
                        </select>
                    </label>
                    <button type="submit">Enviar</button>
                </form>
            </div>
        </>
    );
}

export default MeteorSelection;