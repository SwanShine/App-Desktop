package model;

public class Cliente {
protected String cpf;
protected String Nome;
protected String email;
protected String telefone;
protected String endereço;


public Cliente() {
  }


public Cliente(String cpf, String nome, String email, String telefone, String endereço) {
	super();
	this.cpf = cpf;
	Nome = nome;
	this.email = email;
	this.telefone = telefone;
	this.endereço = endereço;
  }


public String getCpf() {
	return cpf;
}


public void setCpf(String cpf) {
	this.cpf = cpf;
}


public String getNome() {
	return Nome;
}


public void setNome(String nome) {
	Nome = nome;
}


public String getEmail() {
	return email;
}


public void setEmail(String email) {
	this.email = email;
}


public String getTelefone() {
	return telefone;
}


public void setTelefone(String telefone) {
	this.telefone = telefone;
}


public String getEndereço() {
	return endereço;
}


public void setEndereço(String endereço) {
	this.endereço = endereço;
}




}
