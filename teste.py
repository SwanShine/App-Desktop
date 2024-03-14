from tkinter import *
from tkinter import messagebox

def on_enter(e):
    if code.get() == 'Senha':
        code.delete(0, 'end')
        
def on_leave(e):
    if code.get() == '':
        code.insert(0, 'Senha')

def minimize_window(event):
    root.iconify()  # Minimiza a janela principal ao pressionar Esc

def minimize_screen(event):
    screen.iconify()  # Minimiza a janela secundária ao pressionar Esc

def signin():
    usuario = entry_usuario.get()
    senha = code.get()

    if usuario == 'admin' and senha == 'bmvl.wt':
        global screen
        screen = Toplevel(root)
        screen.title('App')
        screen.attributes('-fullscreen', True)
        screen.config(bg='white')

        Label(screen, text='Olá administrador, Bem Vindo de volta!', bg='#fff', font=('Calibri', 20, 'bold')).pack()

        # Bind para minimizar a janela secundária quando a tecla "Esc" for pressionada
        screen.bind("<Escape>", minimize_screen)

        screen.mainloop()
    else:
        messagebox.showerror('Invalid Access', 'Acesso Negado! Usuário e senha Inválida')

root = Tk()
root.title('Login')
root.attributes('-fullscreen', True)
root.configure(bg='#ffffff')

# Frame para o lado esquerdo (cor branca)
frame_esquerdo = Frame(root, bg='#ffffff')
frame_esquerdo.place(relx=0, rely=0, relwidth=0.55, relheight=1)

# Frame para o lado direito (cor roxa)
frame_direito = Frame(root, bg='#800080')
frame_direito.place(relx=0.55, rely=0, relwidth=0.45, relheight=2)

# Frame para a imagem no lado esquerdo
frame_imagem = Frame(frame_esquerdo, bg='#add8e6')
frame_imagem.place(relx=0.1, rely=0.1)

img = PhotoImage(file='images.png')
label_imagem = Label(frame_imagem, image=img, bg='#add8e6')
label_imagem.pack()

# Frame para o texto no lado direito
frame_texto = Frame(frame_direito, bg='#800080')
frame_texto.place(relx=0.1, rely=0.1)

heading = Label(frame_texto, text='Bem Vindo!', fg="#ffffff", bg='#800080', font=('inter', 30, 'bold'))
heading.pack()

# Frame para o campo de entrada de usuário
frame_usuario = Frame(frame_texto, bg='#800080')
frame_usuario.pack(pady=10)  # Adiciona 10 pixels de espaço acima e abaixo do frame

label_usuario = Label(frame_usuario, text='Usuário:', bg='#800080', fg='white')
label_usuario.pack(side=LEFT)  # Alinha o rótulo à esquerda

entry_usuario = Entry(frame_usuario, bg='white', font=('inter', 15))
entry_usuario.pack(side=RIGHT, padx=70)  # Adiciona 70 pixels de espaço à direita do campo de entrada

# Frame para o campo de entrada de senha
frame_senha = Frame(frame_texto, bg='#800080')
frame_senha.pack(pady=10)  # Adiciona 10 pixels de espaço acima e abaixo do frame

label_senha = Label(frame_senha, text='Senha:', bg='#800080', fg='white')
label_senha.pack(side=LEFT)  # Alinha o rótulo à esquerda

code = Entry(frame_senha, width=25, fg='black', border=0, bg='white', font=('inter', 15), show='*')
code.pack(side=RIGHT, padx=70)  # Adiciona 70 pixels de espaço à direita do campo de entrada
code.insert(0, 'Senha') 
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)

Button(frame_texto, width=39, pady=7, text='Sign in', bg='#502779', fg='white', command=signin).pack()



# Bind para minimizar a janela principal quando a tecla "Esc" for pressionada
root.bind("<Escape>", minimize_window)

root.mainloop()
