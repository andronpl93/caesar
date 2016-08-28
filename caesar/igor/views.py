from django.shortcuts import render
import re




# Create your views here.
def kalk(request):
	if request.method!="POST":
		return render(request, 'igor/kalk.html', {})
	else:
	############### ПОИСК ЧАСТОТЫ БУКВ. Диаграма забавная, так что частота будет выводится при нажатии на любую кнопку
		elita=dict(a='8.17',b='1.49',c='2.78',d='4.25',e='12.7',f='2.23',g='2.02',h='6.09',i='6.97',j='0.15',k='0.77',l='4.03',m='2.41',n='6.75',o='7.51',p='1.93',q='0.1',r='5.99',s='6.33',t='9.06',u='2.76',v='0.98',w='2.36',x='0.15',y='1.97',z='0.05')	
		abc=[chr(i+97) for i in range(26)]												#эталонный алфавит
		text=request.POST.get('lef')						 				 			#Получили текст из textarea.
		text=re.sub(r'[А-Яа-я]','',text)  												#Избавляемся от кириллицы
		text=str(text).lower()                											#В  тз не уточнялось о регистре, так что будут маленькие.
		tex=re.sub(r'[+-/*\\[\]\(\);,\s\d\p]','',text)              			        	#tex хранит только рабочий текст, для этого избавляемся от символов
		if len(tex)==0 and request.POST.get('knopka')!='kidok':																	#если поле пустое, обижаемся и выходим
			return render(request, 'igor/kalk.html', {})
		leng=len(tex)      																#количество букв необходимоe для подсчета частоты
		chastota=[round((tex.count(i)/leng)*100,1) for i in abc]
		norm=[((i-min(chastota))*100/(max(chastota)-min(chastota)))+1 for i in chastota]#нормирование проводится исключительно для отображениея на диаграме
																						# чтобы наибольний столбик был высотой в 100%, 
																						#а не в свои проценты частоты
		
		paket=[[norm[i],chastota[i],abc[i]] for i in range(26)]							#дальше пакет передается через return
	############Закончили с частотой
	############Обрабатываем нажатие кнопок
		result=''																		#окончательный результат
		lichka=""																		# через выводятся сообщения о том что пользователь криворукий
		rot=0																			# сдвиг
		if request.POST.get("knopka")!='vanga':
			try:																			
				rot=int(request.POST.get("inText"))
				if rot>26:
					rot=rot-(rot//26)*26													#чтобы не шифровать по кругу 
				elif rot<0:
					lichka="Необоходимо заполнить поле 'ROT' целочисленным положительным значением!"
			except ValueError:
				lichka="Необоходимо заполнить поле 'ROT' целочисленным положительным значением!"
				rot=-1
	################# шифровка
		if request.POST.get("knopka")=='decoder' and rot>=0:
			for i in text:
				if ord(i)<=ord("z") and ord(i)>=ord("a"):								#эти костыли нужны из-за того что в тексте остались пробелы и т.д.
					if ord(i)-rot<ord('a'):
						result+=chr(ord(i)-rot+26)
					else:
						result+=chr(ord(i)-rot)
				else:
					result+=i
	################# расшифровка
		elif request.POST.get("knopka")=='encoder' and rot>=0:
			for i in text:
				if ord(i)<=ord("z") and ord(i)>=ord("a"):
					if ord(i)+rot>ord('z'):
						result+=chr(ord(i)+rot-26)
					else:
						result+=chr(ord(i)+rot)
				else:
					result+=i
	###########перекидываем текст из поля в поле
		elif request.POST.get("knopka")=='kidok':
			if request.POST.get('rig')!='':
				text=request.POST.get('rig')
	############## угадываем	
		elif rot>=0:
			lichka=""
			rot=""
			mi=0;
			Mi=2600
			kek="";
			for i in range(26):
				for j in range(26):
					mi+=abs(float(elita[abc[j]])-chastota[(j+i)-((j+i)//26)*26])
				if mi<Mi:
					Mi=mi
					kek=i
				mi=0
			if kek==0:
				lichka="Судя по всему, данный текс не зашифрован"
			else:
				lichka="Звезды говорят, что нужно расшифровывать с ключом ROT"+str(kek)
		return render(request, 'igor/kalk.html', {'lef':text,'rig':result,'paket':paket,'lichka':lichka,'rot':rot})
