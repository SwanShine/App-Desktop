package model;

import javax.swing.table.AbstractTableModel;

public class ModeloTabela extends AbstractTableModel {
	
	private static final String[] colunas = {
		"CPF", "Nome", "E-mail", "Telefone", "Endere\u00E7o"
		};
	private ArrayList<Cliente> clientes;
	
	@Override
	public int getRowCount() {
		return clientes.size();
	}

	@Override
	public int getColumnCount() {
		return colunas.length;
	}

	@Override
	public Object getValueAt(int rowIndex, int columnIndex) {
		// TODO Auto-generated method stub
		Cliente cliente = clientes.get(rowIndex);
		if(columnIndex == 0) {
			return cliente.getCPF();
		} else
			if(columnIndex == 1) {
				return cliente.getNome();
			} else
				if(columnIndex == 2) {
					return cliente.getEmail();
				} else
					if(columnIndex == 3) {
						return cliente.getTelefone();
					} else
						if(columnIndex == 4) {
							return cliente.getEndereco();
						} else
							if(columnIndex == 0) {
								return cliente.getCPF();
							} else
								if(columnIndex == 0) {
									return cliente.getCPF();
								} else {
									return null;
								}
}

	public ModeloTabela(ArrayList<Cliente> clientes) {
		super();
		this.clientes = clientes;
	}