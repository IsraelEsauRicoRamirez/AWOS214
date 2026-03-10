import React, { useState } from "react";
import {
View,
Text,
TextInput,
FlatList,
StyleSheet,
TouchableOpacity,
ActivityIndicator,
Alert,
ScrollView
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


// GET
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


// POST
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


// PUT
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


// DELETE
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

<View style={styles.container}>

<Text style={styles.titulo}>Gestión de Usuarios</Text>

<ScrollView showsVerticalScrollIndicator={false}>

<View style={styles.formCard}>

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

{loading && <ActivityIndicator size="large" color="#1b5e20" style={{marginTop:20}} />}

<FlatList
data={usuarios}
scrollEnabled={false}
keyExtractor={(item)=>item.id.toString()}
renderItem={({item}) => (

<View style={styles.userCard}>

<View>
<Text style={styles.userName}>{item.nombre}</Text>
<Text style={styles.userInfo}>ID: {item.id}</Text>
<Text style={styles.userInfo}>Edad: {item.edad}</Text>
</View>

<TouchableOpacity
style={styles.deleteBtn}
onPress={()=> eliminarUsuario(item.id)}
>
<Text style={styles.deleteText}>Eliminar</Text>
</TouchableOpacity>

</View>

)}
/>

</ScrollView>

</View>

)

}



const styles = StyleSheet.create({

container:{
flex:1,
backgroundColor:"#f2f4f7",
padding:20
},

titulo:{
fontSize:28,
fontWeight:"bold",
textAlign:"center",
marginBottom:20,
color:"#1b5e20"
},

formCard:{
backgroundColor:"#fff",
borderRadius:15,
padding:15,
marginBottom:20,
alignSelf:"center",
width:"70%",
shadowColor:"#000",
shadowOpacity:0.15,
shadowRadius:6,
elevation:4
},

input:{
backgroundColor:"#f4f4f4",
padding:10,
borderRadius:8,
marginBottom:10,
fontSize:14
},

btn:{
backgroundColor:"#2e7d32",
padding:10,
borderRadius:8,
marginTop:6,
alignItems:"center"
},

btnText:{
color:"#fff",
fontWeight:"bold",
fontSize:14
},

userCard:{
backgroundColor:"#fff",
borderRadius:12,
padding:15,
marginBottom:12,
flexDirection:"row",
justifyContent:"space-between",
alignItems:"center",
shadowColor:"#000",
shadowOpacity:0.1,
shadowRadius:5,
elevation:3
},

userName:{
fontSize:16,
fontWeight:"bold",
color:"#1b5e20"
},

userInfo:{
fontSize:13,
color:"#555"
},

deleteBtn:{
backgroundColor:"#c62828",
paddingVertical:6,
paddingHorizontal:12,
borderRadius:6
},

deleteText:{
color:"#fff",
fontWeight:"bold",
fontSize:13
}

});