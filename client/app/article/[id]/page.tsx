"use client"

import { useRouter } from "next/navigation"
import { useState } from "react"

export interface articleData{
	id: number
	link: string
	title: string
	content: string
	created: string
	sentiment: number
	department: string
}

export default function Page({ params }: { params: { id: string } }) {

	const router = useRouter()
	const [article, setArticle] = useState<articleData>({
		id: -1,
		link: "",
		title: "",
		content: "",
		created: "",
		sentiment: 0,
		department: ""
	})

	async function getData(){
		const req = await fetch(`/api/getart?id=${ params.id }`, {
			method: "GET"
		})
		
		const responseObject = await req.json()
		if (responseObject.status == "fail"){
			router.push("/dashboard")
		}
		setArticle(responseObject.data);
	}

	return (
		<div>
			<div>{ article.title }</div>
			<div>{ article.created }</div>
			<div>{ article.content }</div>
			<div>{ article.link }</div>
		</div>
	)
}