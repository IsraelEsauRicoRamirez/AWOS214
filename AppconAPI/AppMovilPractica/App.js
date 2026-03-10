import React, { useState } from "react";
import {
View,
Text,
TextInput,
FlatList,
StyleSheet,
ImageBackground,
TouchableOpacity,
ActivityIndicator,
Alert
} from "react-native";

import axios from "axios";

export default function App(){


const API = "http://localhost:5000/v1/usuarios/";

const [usuarios,setUsuarios] = useState([]);
const [loading,setLoading] = useState(false);

const [id,setId] = useState("");
const [nombre,setNombre] = useState("");
const [edad,setEdad] = useState("");



const limpiarCampos = ()=>{
setId("")
setNombre("")
setEdad("")
}


// GET usuarios
const obtenerUsuarios = async () => {

setLoading(true)

try{

const res = await axios.get(API)

if(res.data && res.data.usuarios){
setUsuarios(res.data.usuarios)
}

}catch(error){

Alert.alert("Error","No se pudieron obtener usuarios")

}

setLoading(false)

}



// POST crear usuario
const crearUsuario = async () => {

if(!id || !nombre || !edad){
Alert.alert("Error","Completa todos los campos")
return
}

const usuario = {
id:Number(id),
nombre:nombre,
edad:Number(edad)
}

setLoading(true)

try{

await axios.post(API,usuario)

Alert.alert("Usuario creado")

limpiarCampos()

obtenerUsuarios()

}catch(error){

let mensaje="Error al crear"

if(error.response){
mensaje=error.response.data.detail
}

Alert.alert("Error",mensaje)

}

setLoading(false)

}



// PUT actualizar
const actualizarUsuario = async () => {

if(!id){
Alert.alert("Error","Ingresa el ID")
return
}

const usuario = {
nombre:nombre,
edad:Number(edad)
}

setLoading(true)

try{

await axios.put(API + id,usuario)

Alert.alert("Usuario actualizado")

limpiarCampos()

obtenerUsuarios()

}catch(error){

let mensaje="No se pudo actualizar"

if(error.response){
mensaje=error.response.data.detail
}

Alert.alert("Error",mensaje)

}

setLoading(false)

}



// DELETE usuario
const eliminarUsuario = async (usuarioId) => {

setLoading(true)

try{

await axios.delete(API + usuarioId)

Alert.alert("Usuario eliminado")

obtenerUsuarios()

}catch(error){

Alert.alert("Error","No se pudo eliminar")

}

setLoading(false)

}



return(

<ImageBackground
source={require("./assets/bosque.jpg")}
style={styles.background}
imageStyle={{resizeMode:"cover"}}
>

<View style={styles.overlay}>

<Text style={styles.titulo}>Gestión de Usuarios</Text>


<TextInput
style={styles.input}
placeholder="ID"
keyboardType="numeric"
value={id}
onChangeText={setId}
/>

<TextInput
style={styles.input}
placeholder="Nombre"
value={nombre}
onChangeText={setNombre}
/>

<TextInput
style={styles.input}
placeholder="Edad"
keyboardType="numeric"
value={edad}
onChangeText={setEdad}
/>


<View style={styles.botones}>

<TouchableOpacity style={styles.btn} onPress={obtenerUsuarios}>
<Text style={styles.btnText}>Obtener Usuarios</Text>
</TouchableOpacity>

<TouchableOpacity style={styles.btn} onPress={crearUsuario}>
<Text style={styles.btnText}>Crear Usuario</Text>
</TouchableOpacity>

<TouchableOpacity style={styles.btn} onPress={actualizarUsuario}>
<Text style={styles.btnText}>Actualizar Usuario</Text>
</TouchableOpacity>

</View>


{loading && <ActivityIndicator size="large" color="#2e7d32" />}


<FlatList
data={usuarios}
keyExtractor={(item)=>item.id.toString()}
renderItem={({item}) => (

<View style={styles.card}>

<Text style={styles.cardText}>ID: {item.id}</Text>
<Text style={styles.cardText}>Nombre: {item.nombre}</Text>
<Text style={styles.cardText}>Edad: {item.edad}</Text>

<TouchableOpacity
style={styles.deleteBtn}
onPress={()=> eliminarUsuario(item.id)}
>

<Text style={styles.deleteText}>Eliminar</Text>

</TouchableOpacity>

</View>

)}
/>

</View>

</ImageBackground>

)

}



const styles = StyleSheet.create({

background:{
flex:1,
width:"100%",
height:"100%"
},

overlay:{
flex:1,
backgroundColor:"rgba(255,255,255,0.9)",
padding:20
},

titulo:{
fontSize:30,
fontWeight:"bold",
textAlign:"center",
marginBottom:20,
color:"#1b5e20"
},

input:{
borderWidth:1,
padding:10,
marginBottom:10,
borderRadius:6,
backgroundColor:"#fff"
},

botones:{
marginBottom:10
},

btn:{
backgroundColor:"#2e7d32",
padding:12,
marginBottom:10,
borderRadius:6,
alignItems:"center"
},

btnText:{
color:"#fff",
fontWeight:"bold"
},

card:{
backgroundColor:"#ffffff",
padding:15,
marginTop:10,
borderRadius:8,
borderWidth:1,
borderColor:"#ddd"
},

cardText:{
fontSize:16
},

deleteBtn:{
backgroundColor:"#c62828",
padding:8,
marginTop:10,
borderRadius:5,
alignItems:"center"
},

deleteText:{
color:"#fff",
fontWeight:"bold"
}

});